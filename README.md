# VK Keywords Parser

Парсер для сбора ключевых слов из сообществ ВКонтакте (названия, описания, посты, товары).  
Использует **Selenium** для парсинга и **pymorphy3** для нормализации слов.

## 📌 Возможности
- Сбор текстов из заданных сообществ (название, описание, посты, товары).
- Извлечение биграмм и триграмм (2-3 словные ключевые фразы).
- Сохранение результатов в `vk_keywords.csv`.

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

1. Создай файл `.env` в корне проекта:
   ```env
   VK_GROUPS=имя сообщества1,имя сообщества2
   ```

2. Добавь `.env` в `.gitignore`, чтобы он не попал в репозиторий.

## 🚀 Запуск

```bash
python parser.py
```

После выполнения в папке появится файл:

- `vk_keywords.csv` — топ ключевых фраз.

В консоли будет показан ТОП-50 фраз.

## 📂 Пример вывода

```
ТОП-50 фраз:
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
- python-dotenv

Устанавливаются автоматически через `requirements.txt`.
