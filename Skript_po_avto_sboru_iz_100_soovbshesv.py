import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SEARCH_QUERY = "кухни на заказ"

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--headless")  # если не нужен интерфейс

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

print("🔍 Открываем поиск...")
search_url = f"https://vk.com/search?c[q]={SEARCH_QUERY}&c[section]=communities"
driver.get(search_url)

try:
    # ждём ссылку, внутри которой встречается текст "кухни"
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@href,'search_track_code')][.//text()[contains(., 'кухни')]]"))
    )
    href = element.get_attribute("href")
    name = element.text.strip()
    print("✅ Нашли сообщество:", name)
    print("🔗 Ссылка:", href)

except Exception as e:
    print("⚠️ Ошибка:", e)

time.sleep(3)
driver.quit()
