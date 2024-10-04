# bot/bot.py

from telegram.ext import Application, CommandHandler, CallbackQueryHandler  # Импортируем необходимые классы для работы с ботом Telegram
from .handlers import (  # Импортируем обработчики команд и callback-функций из модуля handlers
    register_start_command,
    register_callback,
    handle_start_command,
    view_analytics_handler,
    analytics_handler
)
from config import TELEGRAM_BOT_TOKEN  # Импортируем токен бота из конфигурационного файла


def main():
    """
    Основная функция для настройки и запуска Telegram-бота.

    1. Создает экземпляр приложения Telegram-бота с переданным токеном.
    2. Регистрирует обработчики команд и callback-функций.
    3. Запускает приложение в режиме polling для получения и обработки обновлений.
    """
    # Создаем экземпляр приложения Telegram-бота с переданным токеном
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", register_start_command, filters=None))  # Обработчик команды /start для регистрации
    application.add_handler(CommandHandler("start", handle_start_command))  # Обработчик команды /start для обработки логики старта

    # Регистрируем обработчики callback-запросов
    application.add_handler(CallbackQueryHandler(register_callback, pattern='register'))  # Обработчик callback для регистрации пользователя
    application.add_handler(CallbackQueryHandler(view_analytics_handler, pattern='view_analytics'))  # Обработчик callback для просмотра аналитики
    application.add_handler(CallbackQueryHandler(analytics_handler))  # Обработчик callback для нажатия кнопок выбора периодов аналитики

    # Запуск бота в режиме polling
    application.run_polling()


if __name__ == '__main__':
    # Запуск основной функции при запуске модуля
    main()
