# bot/bot.py

from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from .handlers import register_start_command, register_callback, handle_start_command, view_analytics_handler, analytics_handler  # Импортируем analytics_handler
from config import TELEGRAM_BOT_TOKEN


def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", register_start_command, filters=None))
    application.add_handler(CommandHandler("start", handle_start_command))

    application.add_handler(CallbackQueryHandler(register_callback, pattern='register'))
    application.add_handler(CallbackQueryHandler(view_analytics_handler, pattern='view_analytics'))
    application.add_handler(CallbackQueryHandler(analytics_handler))  # Обработчик для нажатия кнопок периодов аналитики

    application.run_polling()


if __name__ == '__main__':
    main()
