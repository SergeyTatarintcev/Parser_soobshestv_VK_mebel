import requests
import time
import pandas as pd
from datetime import datetime, timedelta

# 👉 ВСТАВЬ сюда свой сервисный ключ доступа
TOKEN = "56bb3d8356bb3d8356bb3d8381558cd7fb556bb56bb3d833e349bfe86257f84d0c1dbef"
API_URL = "https://api.vk.com/method/"
VERSION = "5.199"

# Ключевые слова для поиска сообществ
SEARCH_QUERIES = ["кухни", "кухни на заказ", "мебель", "корпусная мебель"]

# Сколько сообществ брать на каждый запрос
PER_QUERY = 100

# Отсечка по дате (посты не старше месяца)
cutoff_date = int((datetime.now() - timedelta(days=30)).timestamp())

results = []

def vk_api(method, params):
    params.update({"access_token": TOKEN, "v": VERSION})
    r = requests.get(API_URL + method, params=params).json()
    if "response" in r:
        return r["response"]
    else:
        print("Ошибка:", r)
        return None

print("🔍 Ищем сообщества...")

for query in SEARCH_QUERIES:
    groups = vk_api("groups.search", {
        "q": query,
        "count": PER_QUERY,
        "country_id": 1  # РФ
    })
    if not groups:
        continue

    for g in groups["items"]:
        group_id = g["id"]

        # Получаем информацию о группе (включая контакты)
        info = vk_api("groups.getById", {
            "group_id": group_id,
            "fields": "contacts,activity,members_count,screen_name"
        })
        if not info:
            continue
        group = info[0]

        contacts = group.get("contacts", [])
        if not contacts:  # без контактов пропускаем
            continue

        # Проверяем свежесть поста
        wall = vk_api("wall.get", {"owner_id": -group_id, "count": 1})
        if not wall or wall["count"] == 0:
            continue
        last_post = wall["items"][0]
        if last_post["date"] < cutoff_date:
            continue

        # Сохраняем данные
        for c in contacts:
            results.append({
                "group_id": group_id,
                "group_name": group["name"],
                "group_url": f"https://vk.com/{group.get('screen_name')}",
                "members_count": group.get("members_count", 0),
                "contact_id": c.get("user_id"),
                "desc": c.get("desc")
            })

        print(f"✅ {group['name']} — добавлено")

        time.sleep(0.34)  # чтобы не превысить лимит API

# Сохраняем в CSV
df = pd.DataFrame(results)
df.to_csv("all_mebel_aktiv.csv", index=False, encoding="utf-8-sig")

print("🔥 Готово! Сохранено:", len(results), "записей в all_mebel_aktiv.csv")
