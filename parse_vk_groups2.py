import os
import re
import time
import pandas as pd
from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import pymorphy3

# Загружаем переменные окружения
load_dotenv()
groups_file = os.getenv("VK_GROUPS_FILE", "Lists 640.xlsx")

# Читаем список сообществ из Excel (столбец А)
df_groups = pd.read_excel(groups_file)
groups = df_groups.iloc[:, 0].dropna().astype(str).tolist()

print(f"📂 Загружено {len(groups)} сообществ из '{groups_file}'")

# Морфоанализатор для нормализации слов
morph = pymorphy3.MorphAnalyzer()

def normalize_word(word: str) -> str:
    return morph.parse(word)[0].normal_form

def extract_phrases(text: str, n: int = 2):
    """Извлекаем биграммы и триграммы"""
    words = re.findall(r"[а-яa-zё]+", text.lower())
    stop = {"и","в","на","с","по","а","но","или","как","к","что","это","от","для","из","под","при","над","у","же","бы","то"}
    words = [normalize_word(w) for w in words if w not in stop and len(w) > 2]
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

# Настройка Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

all_phrases = Counter()

for g in groups:
    g = g.strip()
    if not g:
        continue

    try:
        url = f"https://vk.com/{g}"
        driver.get(url)
        time.sleep(2)

        texts = []

        # Название
        try:
            title = driver.find_element(By.CLASS_NAME, "page_name").text
            texts.append(title)
        except:
            pass

        # Описание
        try:
            desc = driver.find_element(By.CLASS_NAME, "page_description").text
            texts.append(desc)
        except:
            pass

        # Посты
        posts = driver.find_elements(By.CLASS_NAME, "wall_post_text")
        for p in posts[:20]:  # берём первые 20 постов
            texts.append(p.text)

        # Товары
        goods = driver.find_elements(By.CLASS_NAME, "market_row")
        for item in goods[:10]:  # берём первые 10 товаров
            texts.append(item.text)

        full_text = " ".join(texts)

        # Считаем биграммы и триграммы
        for n in [2, 3]:
            all_phrases.update(extract_phrases(full_text, n))

        print(f"✅ Обработано сообщество: {g}")

    except Exception as e:
        print(f"⚠️ Ошибка с {g}: {e}")

driver.quit()

# Сохраняем ТОП-500 ключевых фраз
df = pd.DataFrame(all_phrases.most_common(500), columns=["Фраза", "Частота"])
df.to_csv("vk_keywords_from_groups.csv", index=False, encoding="utf-8-sig")

print("\n🔥 ТОП-30 ключевых фраз:")
for phrase, count in all_phrases.most_common(30):
    print(f"{phrase} — {count}")
