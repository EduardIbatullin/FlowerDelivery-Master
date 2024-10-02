# bot/handlers.py

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from telegram.ext import ContextTypes
from .keyboards import (
    get_register_button_keyboard, get_back_to_profile_keyboard, get_admin_options_keyboard,
    get_not_admin_options_keyboard, get_analytics_period_keyboard
)
from .messages import (
    WELCOME_MESSAGE_NOT_REGISTERED, WELCOME_MESSAGE_NOT_ADMIN, WELCOME_MESSAGE_ADMIN,
    REGISTRATION_SUCCESS, REGISTRATION_ERROR, TELEGRAM_ID_SAVED, USER_NOT_FOUND_ERROR, TELEGRAM_ID_TO_SAVED
)
from .utils import (
    send_post_request, get_sales_analytics, generate_sales_chart, aggregate_sales_data, get_dates_by_period,
    format_date
)
from config import DJANGO_SERVER_URL


async def register_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start, который использует user_id для приветствия пользователя и предлагает регистрацию.
    """
    args = context.args
    if args:
        user_id = args[0]
        response = await send_post_request('users/get_user_data', {'user_id': user_id})

        if response and response.get("status") == "success":
            if response.get('first_name'):
                first_name = response.get('first_name')
            else:
                first_name = response.get('username')
            message_text = TELEGRAM_ID_TO_SAVED.format(username=first_name)
            context.user_data['user_id'] = user_id  # Сохраняем user_id для дальнейшего использования
        else:
            message_text = USER_NOT_FOUND_ERROR
    else:
        await handle_start_command(update, context)
        return

    reply_markup = get_register_button_keyboard()
    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик для нажатия инлайн-кнопки регистрации.
    """
    query = update.callback_query
    await query.answer()

    telegram_id = update.effective_user.id
    user_id = context.user_data.get('user_id')

    if user_id:
        # Отправляем запрос для сохранения telegram_id на сервере Django
        response = await send_post_request('users/save_telegram_id', {'telegram_id': telegram_id, 'user_id': user_id})

        if response and response.get("status") == "success":
            profile_url = f"{DJANGO_SERVER_URL}/users/profile/"
            await query.edit_message_text(text=REGISTRATION_SUCCESS, reply_markup=get_back_to_profile_keyboard(profile_url))
        else:
            await query.edit_message_text(text=REGISTRATION_ERROR)
    else:
        await query.edit_message_text(text="Ошибка: user_id не был найден.")


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start, вызываемой напрямую из бота (без параметров).
    """
    telegram_id = update.effective_user.id
    response = await send_post_request('users/get_user_data_by_telegram_id', {'telegram_id': telegram_id})

    if response and response.get("status") == "success":
        user_data = response.get("user_data", {})
        is_admin = user_data.get("is_admin", False)

        if is_admin:
            message_text = WELCOME_MESSAGE_ADMIN
            reply_markup = get_admin_options_keyboard()
        else:
            message_text = WELCOME_MESSAGE_NOT_ADMIN
            reply_markup = get_not_admin_options_keyboard()

    else:
        message_text = WELCOME_MESSAGE_NOT_REGISTERED
        reply_markup = get_register_button_keyboard()

    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def view_analytics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик нажатия на кнопку "Посмотреть аналитику".
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Пожалуйста, выберите период для просмотра аналитики.", reply_markup=get_analytics_period_keyboard())


async def analytics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    period = query.data  # Получаем период из нажатой кнопки
    await query.answer()  # Ответ на запрос, чтобы убрать индикатор ожидания

    start_date, end_date = get_dates_by_period(period)

    analytics_data = await get_sales_analytics(start_date, end_date, query.from_user.id)

    if not analytics_data or analytics_data.get("status") != "success":
        message_text = "Не удалось получить корректные данные аналитики. Проверьте параметры и повторите запрос."
        await query.edit_message_text(text=message_text)
        return

    # Формирование текстового сообщения с аналитикой
    total_orders = analytics_data.get("total_orders", 0)
    total_revenue = analytics_data.get("total_revenue", 0)
    message_text = f"Аналитика за выбранный период ({period}):\n\n"
    message_text += f"Общее количество заказов: {total_orders} заказов\n"
    message_text += f"Общая выручка: {total_revenue} руб.\n\n"

    # Агрегируем и сортируем данные перед выводом
    aggregated_data = aggregate_sales_data(analytics_data.get("data", []))
    details_text = "Детализация по дням:\n"

    for product in aggregated_data:
        formatted_date = format_date(product['period_start'])
        details_text += f"- {formatted_date}: Продано {product['total_sales']} шт, на сумму {product['total_revenue']} руб.\n"

    # Разбивка текста на блоки по 4096 символов
    split_messages = [details_text[i:i + 4096] for i in range(0, len(details_text), 4096)]

    await query.edit_message_text(text=message_text)

    for msg in split_messages:
        await context.bot.send_message(chat_id=query.message.chat_id, text=msg)

    await send_sales_chart(update, context, analytics_data)


async def send_sales_chart(update: Update, context: ContextTypes.DEFAULT_TYPE, analytics_data):
    buffer = generate_sales_chart(analytics_data)
    chart = InputFile(buffer, filename='sales_chart.png')
    await update.callback_query.message.reply_photo(photo=chart, caption='График продаж за выбранный период.')
    buffer.close()
