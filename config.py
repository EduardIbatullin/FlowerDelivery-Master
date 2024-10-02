# config.py

import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем необходимые переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DJANGO_SERVER_URL = os.getenv('DJANGO_SERVER_URL')

# Если токен не найден, выводим ошибку
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("Не удалось найти TELEGRAM_BOT_TOKEN в .env файле")

if DJANGO_SERVER_URL is None:
    raise ValueError("Не удалось найти DJANGO_SERVER_URL в .env файле")
