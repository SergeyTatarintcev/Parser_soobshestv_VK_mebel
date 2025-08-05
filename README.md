# VK Keywords Parser

Парсер для сбора сообществ и ключевых слов из ВКонтакте.  
Использует **Selenium** для парсинга страниц и **pymorphy3** для нормализации слов.

## 📌 Возможности
- Автоматический поиск сообществ по запросу «кухни на заказ» и сбор их screen_name.
- Сохранение списка групп в файлы `.py` и `.csv`.
- Анализ заданных сообществ (название, описание, посты, товары).
- Извлечение биграмм и триграмм (2–3 словные ключевые фразы).
- Сохранение результатов в `csv`.

## ⚙️ Установка

1. Клонируй репозиторий:
   ```bash
   git clone https://github.com/SergeyTatarintcev/Parser_soobshestv_VK_mebel.git
   cd Parser_soobshestv_VK_mebel
   ```

2. Создай виртуальное окружение:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # для Linux/Mac
   .venv\Scripts\activate      # для Windows
   ```

3. Установи зависимости:
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Настройка

1. Для `parse_vk_groups.py` настройки не нужны — он сам идёт в поиск ВК.
2. Для `parse_vk_groups2.py` нужно указать в `.env` путь до файла Excel:
   ```env
   VK_GROUPS_FILE=Lists 640.xlsx
   ```
   В этом Excel в **первом столбце (А)** должен быть список `screen_name` сообществ.

3. Добавь `.env` и все `.xlsx` файлы в `.gitignore`, чтобы они не попали в репозиторий.

## 🚀 Запуск

### Поиск сообществ
```bash
python parse_vk_groups.py
```
После выполнения появятся:
- `vk_groups_list_name.py` — список screen_name в Python‑формате.
- `vk_groups_list_name.csv` — список screen_name + кликабельные ссылки.

### Сбор ключевых слов
```bash
python parse_vk_groups2.py
```
После выполнения появится:
- `vk_keywords_from_groups.csv` — список топ‑500 ключевых фраз.

В консоли будет показан ТОП‑30.

## 📂 Пример вывода

```
ТОП-30 ключевых фраз:
кухня заказ — 42
заказать кухню — 38
угловой кухня — 27
белый кухня — 19
...
```

## 📦 Зависимости

- selenium
- webdriver-manager
- pymorphy3
- pandas
- openpyxl
- python-dotenv

Устанавливаются автоматически через `requirements.txt`.


## 👨‍💻 Автор

Сделано [SergeyTatarintcev](https://github.com/SergeyTatarintcev)