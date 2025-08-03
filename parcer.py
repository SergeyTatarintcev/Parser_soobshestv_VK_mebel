import time
import re
import os
from collections import Counter
import pandas as pd
import pymorphy3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
groups = os.getenv("VK_GROUPS", "").split(",")

# морфоанализатор
morph = pymorphy3.MorphAnalyzer()

def normalize_word(word):
    return morph.parse(word)[0].normal_form

def extract_phrases(text, n=2):
    """Извлекаем биграммы/триграммы"""
    words = re.findall(r"[а-яa-zё]+", text.lower())
    stop = {"и","в","на","с","по","а","но","или","как","к","что","это","от","для","из","под","при","над","у","же","бы","то"}
    words = [normalize_word(w) for w in words if w not in stop and len(w) > 2]
    return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

# Selenium
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
        time.sleep(3)

        texts = []

        # название
        try:
            title = driver.find_element(By.CLASS_NAME, "page_name").text
            texts.append(title)
        except:
            pass

        # описание
        try:
            desc = driver.find_element(By.CLASS_NAME, "page_description").text
            texts.append(desc)
        except:
            pass

        # посты
        posts = driver.find_elements(By.CLASS_NAME, "wall_post_text")
        for p in posts[:30]:
            texts.append(p.text)

        # товары
        goods = driver.find_elements(By.CLASS_NAME, "market_row")
        for item in goods:
            texts.append(item.text)

        full_text = " ".join(texts)

        for n in [2,3]:
            all_phrases.update(extract_phrases(full_text, n))

        print(f"✅ Собрано: {g}")

    except Exception as e:
        print(f"Ошибка с {g}: {e}")

driver.quit()

# сохраняем в CSV
df = pd.DataFrame(all_phrases.most_common(300), columns=["Фраза", "Частота"])
df.to_csv("vk_keywords.csv", index=False, encoding="utf-8-sig")

print("\nТОП-50 фраз:")
for phrase, count in all_phrases.most_common(50):
    print(f"{phrase} — {count}")
