import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Поисковый запрос
SEARCH_URL = "https://vk.com/search?c[q]=кухни на заказ&c[section]=communities"

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # фоновый режим
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(SEARCH_URL)

time.sleep(3)

print("🔍 Открыли поиск... начинаем скролл")

last_height = driver.execute_script("return document.body.scrollHeight")
scroll_rounds = 0
max_scrolls = 30  # ограничение, чтобы не крутить бесконечно

while scroll_rounds < max_scrolls:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # если страница не растёт — конец
        print("⚠️ Достигли конца списка.")
        break
    last_height = new_height
    scroll_rounds += 1
    print(f"⬇️ Прокрутка {scroll_rounds}")

# Собираем ссылки на сообщества
links = driver.find_elements(By.XPATH, "//a[contains(@href,'/public') or contains(@href,'/club') or contains(@href,'/')]")

group_names = []
for link in links:
    href = link.get_attribute("href")
    if href and "vk.com/" in href:
        # оставляем только screen_name
        name = href.split("vk.com/")[-1].split("?")[0].strip("/")
        # фильтруем мусорные ссылки
        if name and all(x not in name for x in ["feed", "search", "join", "write"]):
            if name not in group_names:
                group_names.append(name)

driver.quit()

print("\n✅ Собрано сообществ:", len(group_names))
print(group_names)

# Сохраним в Python файл
with open("vk_groups_list.py", "w", encoding="utf-8") as f:
    f.write("groups = " + str(group_names))

# Сохраним в CSV
df = pd.DataFrame(group_names, columns=["group_name"])
df.to_csv("vk_groups_list.csv", index=False, encoding="utf-8-sig")

print("\n📂 Список сохранён в vk_groups_list.py и vk_groups_list.csv")
