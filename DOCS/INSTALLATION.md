# Установка и настройка

## Навигация
- [К началу](../README.md)
- [Использование](./USAGE.md)
- [Архитектура проекта](./ARCHITECTURE.md)
- [Оптимизация](./OPTIMIZATION.md)
- [Решение проблем](./TROUBLESHOOTING.md)
- [Содействие развитию проекта](./CONTRIBUTING.md)

## Системные требования
- Python >= 3.8
- Django >= 5.1.1
- SQLite (используется по умолчанию)
- Redis >= 6.0 (для кэширования и улучшения производительности)

## Установка проекта

1. Склонируйте репозиторий:
    ```bash
    git clone https://github.com/EduardIbatullin/FlowerDelivery-Master.git
    ```

2. Перейдите в директорию проекта:
    ```bash
    cd FlowerDelivery-Master
    ```

3. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

4. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

5. Выполните миграции:
    ```bash
    python manage.py migrate
    ```

6. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

7. В корневой директории проекта создайте файл `.env` со следующим содержимым:

    ```plaintext
    # Токен вашего Telegram-бота. Сгенерируйте свой токен в @BotFather.
    TELEGRAM_BOT_TOKEN='ваш_токен'

    # Уникальный секретный ключ Django. Сгенерируйте свой с помощью команды:
    # python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    SECRET_KEY='ваш_секретный_ключ'

    # Включение режима отладки. Используйте True для разработки и False для продакшена.
    DEBUG=True

    # Разрешенные хосты. Укажите хосты, которые могут обращаться к проекту.
    ALLOWED_HOSTS=localhost,127.0.0.1

    # URL вашего Django-сервера. Обычно используется для взаимодействия с ботом.
    DJANGO_SERVER_URL='http://127.0.0.1:8000'
    ```

    > **Примечание:** Не добавляйте `SECRET_KEY` и другие конфиденциальные данные в публичный репозиторий GitHub. Храните эти данные только в `.env` файле, а сам файл добавьте в `.gitignore`.

8. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

9. Перейдите по адресу `http://127.0.0.1:8000` для проверки работы.

## Запуск Telegram-бота

Telegram-бот необходимо запускать отдельно от сервера Django:

1. Войдите в директорию с ботом:
    ```bash
    cd bot
    ```

2. Запустите бота:
    ```bash
    python bot.py
    ```

3. Проверьте работоспособность бота в Telegram.

## Настройка интеграции с Telegram-ботом

1. Убедитесь, что переменная `TELEGRAM_BOT_TOKEN` указана в файле `.env`:
    ```plaintext
    TELEGRAM_BOT_TOKEN='ваш_токен'
    ```

2. Перезапустите сервер и бот для применения изменений.
