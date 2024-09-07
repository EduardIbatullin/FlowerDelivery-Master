import logging
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

# Получение токена из переменной окружения
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Включаем ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# Команда start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Здравствуйте! Я бот для заказа цветов. Вот что я умею:\n"
        "/catalog - Просмотреть каталог цветов\n"
        "/cart - Просмотреть корзину\n"
        "/orders - Проверить статус ваших заказов\n"
        "/help - Помощь"
    )


# Основная функция
def main() -> None:
    # Убедитесь, что токен успешно загружен
    if not TELEGRAM_BOT_TOKEN:
        logger.error("Не удалось загрузить TELEGRAM_BOT_TOKEN из .env файла")
        return

    updater = Updater(TELEGRAM_BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
