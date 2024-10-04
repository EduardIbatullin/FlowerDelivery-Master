# bot/handlers.py

from telegram import Update, InputFile  # Импорт классов для работы с обновлениями и элементами интерфейса Telegram
from telegram.ext import ContextTypes  # Импорт контекстного типа для асинхронных вызовов бота
from .keyboards import (  # Импортируем клавиатуры для формирования пользовательских интерфейсов в боте
    get_register_button_keyboard,
    get_back_to_profile_keyboard,
    get_admin_options_keyboard,
    get_not_admin_options_keyboard,
    get_analytics_period_keyboard
)
from .messages import (  # Импортируем текстовые сообщения, используемые в ответах бота
    WELCOME_MESSAGE_NOT_REGISTERED,
    WELCOME_MESSAGE_NOT_ADMIN,
    WELCOME_MESSAGE_ADMIN,
    REGISTRATION_SUCCESS,
    REGISTRATION_ERROR,
    USER_NOT_FOUND_ERROR,
    TELEGRAM_ID_TO_SAVED
)
from .utils import (  # Импортируем утилиты для отправки запросов, получения аналитики и генерации графиков
    send_post_request,
    get_sales_analytics,
    generate_sales_chart,
    aggregate_sales_data,
    get_dates_by_period,
    format_date
)
from config import DJANGO_SERVER_URL  # Импортируем URL сервера Django из конфигурационного файла


async def register_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start, который использует user_id для приветствия пользователя и предлагает регистрацию.

    Аргументы:
        update: Объект обновления от Telegram, который содержит информацию о сообщении.
        context: Контекст для управления данными, связанными с этим обновлением.

    Логика:
    - Проверяет, передан ли `user_id` в аргументах команды.
    - Если передан, отправляет запрос на сервер Django для получения данных пользователя.
    - Если данные пользователя получены успешно, формирует сообщение с предложением зарегистрироваться.
    - Если `user_id` отсутствует или данные не найдены, вызывает стандартный обработчик `handle_start_command`.

    Ожидаемый результат:
    - Сообщение с предложением зарегистрироваться и кнопкой для регистрации.
    - В случае ошибки — сообщение об ошибке.
    """
    args = context.args
    if args:
        user_id = args[0]
        # Отправляем запрос на сервер для получения данных пользователя по user_id
        response = await send_post_request('users/get_user_data', {'user_id': user_id})

        # Проверяем успешность получения данных пользователя
        if response and response.get("status") == "success":
            first_name = response.get('first_name', response.get('username'))
            message_text = TELEGRAM_ID_TO_SAVED.format(username=first_name)
            context.user_data['user_id'] = user_id  # Сохраняем user_id для дальнейшего использования
        else:
            message_text = USER_NOT_FOUND_ERROR
    else:
        # Если нет аргументов, вызываем стандартный обработчик
        await handle_start_command(update, context)
        return

    reply_markup = get_register_button_keyboard()
    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик нажатия инлайн-кнопки для регистрации пользователя в боте.

    Аргументы:
        update: Объект обновления от Telegram.
        context: Контекст для сохранения и управления данными.

    Логика:
    - Извлекает telegram_id и user_id из переданных данных.
    - Отправляет запрос на сервер Django для сохранения `telegram_id`.
    - Если сохранение успешно, выводит сообщение об успешной регистрации.
    - В случае ошибки выводит сообщение об ошибке.

    Ожидаемый результат:
    - Сообщение с подтверждением успешной регистрации.
    - В случае ошибки — сообщение с текстом ошибки.
    """
    query = update.callback_query
    await query.answer()  # Подтверждаем получение callback

    telegram_id = update.effective_user.id
    user_id = context.user_data.get('user_id')

    # Проверяем, что user_id был сохранен в предыдущем шаге
    if user_id:
        # Отправляем запрос для сохранения telegram_id на сервере Django
        response = await send_post_request('users/save_telegram_id', {'telegram_id': telegram_id, 'user_id': user_id})

        if response and response.get("status") == "success":
            profile_url = f"{DJANGO_SERVER_URL}/users/profile/"
            await query.edit_message_text(text=REGISTRATION_SUCCESS,
                                          reply_markup=get_back_to_profile_keyboard(profile_url))
        else:
            await query.edit_message_text(text=REGISTRATION_ERROR)
    else:
        await query.edit_message_text(text="Ошибка: user_id не был найден.")


async def handle_start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start, вызываемой напрямую из бота (без параметров).

    Аргументы:
        update: Объект обновления от Telegram.
        context: Контекст для управления данными.

    Логика:
    - Выполняет запрос на сервер Django для получения данных пользователя по telegram_id.
    - Формирует приветственное сообщение и кнопки для администраторов или обычных пользователей.
    - Если пользователь не зарегистрирован, предлагает регистрацию.

    Ожидаемый результат:
    - Приветственное сообщение и соответствующая клавиатура с опциями в зависимости от роли пользователя.
    """
    telegram_id = update.effective_user.id
    response = await send_post_request('users/get_user_data_by_telegram_id', {'telegram_id': telegram_id})

    # Проверяем, был ли запрос успешным
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
        # Если пользователь не зарегистрирован, предлагаем регистрацию
        message_text = WELCOME_MESSAGE_NOT_REGISTERED
        reply_markup = get_register_button_keyboard()

    await update.message.reply_text(message_text, reply_markup=reply_markup)


async def view_analytics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик нажатия на кнопку "Посмотреть аналитику".

    Аргументы:
        update: Объект обновления от Telegram.
        context: Контекст для управления данными.

    Логика:
    - Отвечает на callback запрос и отображает кнопки для выбора периода аналитики.

    Ожидаемый результат:
    - Сообщение с запросом выбора периода и клавиатурой с опциями.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Пожалуйста, выберите период для просмотра аналитики.",
                                  reply_markup=get_analytics_period_keyboard())


async def analytics_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик выбора периода аналитики и получения данных.

    Аргументы:
        update: Объект обновления от Telegram.
        context: Контекст для управления данными.

    Логика:
    - Получает выбранный период и отправляет запрос на сервер Django.
    - Если данные успешны, выводит сообщение с детализированной аналитикой и отправляет график.

    Ожидаемый результат:
    - Сообщение с аналитическими данными.
    - Отправка графика продаж.
    """
    query = update.callback_query
    period = query.data  # Получаем период из нажатой кнопки
    await query.answer()  # Ответ на запрос, чтобы убрать индикатор ожидания

    start_date, end_date = get_dates_by_period(period)
    analytics_data = await get_sales_analytics(start_date, end_date, query.from_user.id)

    # Проверяем корректность полученных данных аналитики
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

    # Отправляем подробности аналитики в виде отдельных сообщений
    for msg in split_messages:
        await context.bot.send_message(chat_id=query.message.chat_id, text=msg)

    # Отправляем график с аналитикой
    await send_sales_chart(update, context, analytics_data)


async def send_sales_chart(update: Update, context: ContextTypes.DEFAULT_TYPE, analytics_data):
    """
    Отправка графика продаж в виде изображения.

    Аргументы:
        update: Объект обновления от Telegram.
        context: Контекст для управления данными.
        analytics_data: Данные аналитики для построения графика.

    Логика:
    - Генерирует график продаж и отправляет его пользователю.

    Ожидаемый результат:
    - Сообщение с изображением графика продаж.
    """
    buffer = generate_sales_chart(analytics_data)
    chart = InputFile(buffer, filename='sales_chart.png')
    await update.callback_query.message.reply_photo(photo=chart, caption='График продаж за выбранный период.')
    buffer.close()
