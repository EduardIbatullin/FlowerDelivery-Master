# bot/utils.py

import aiohttp  # Импорт библиотеки для выполнения асинхронных HTTP-запросов
import matplotlib.pyplot as plt  # Импорт библиотеки для создания графиков и диаграмм
from io import BytesIO  # Импорт класса для работы с байтовыми объектами в памяти
from config import DJANGO_SERVER_URL, TELEGRAM_BOT_TOKEN  # Импорт URL сервера Django и токена Telegram из конфигурационного файла
from datetime import datetime  # Импорт класса datetime для работы с датами

# URL API Telegram для отправки сообщений
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


async def send_telegram_message(chat_id, text):
    """
    Отправляет сообщение в Telegram через Telegram API.

    Аргументы:
        chat_id (int): Идентификатор чата для отправки сообщения.
        text (str): Текст сообщения.

    Логика:
    - Создает сессию HTTP-запроса и отправляет POST-запрос на Telegram API.
    - Проверяет статус ответа и возвращает ошибку при неуспешной отправке.

    Исключения:
    - aiohttp.ClientError: Ошибка соединения с API Telegram.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                TELEGRAM_API_URL,
                json={"chat_id": chat_id, "text": text},
                timeout=10
            ) as response:
                if response.status != 200:
                    raise Exception(f"Ошибка при отправке сообщения в Telegram: {await response.text()}")
    except aiohttp.ClientError as e:
        raise Exception(f"Ошибка соединения с Telegram API: {str(e)}")


async def send_post_request(endpoint, data):
    """
    Отправляет POST-запрос на сервер Django и возвращает ответ в формате JSON.

    Аргументы:
        endpoint (str): Конечная точка API на сервере Django.
        data (dict): Данные для отправки в теле запроса.

    Возвращает:
        dict или None: Ответ сервера в формате JSON или None при ошибке соединения.
    """
    url = f"{DJANGO_SERVER_URL}/{endpoint}/"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except aiohttp.ClientError:
        return None


async def get_sales_analytics(start_date, end_date, telegram_id, product_id=None):
    """
    Выполняет запрос на сервер Django для получения данных аналитики продаж.

    Аргументы:
        start_date (str): Начальная дата периода аналитики.
        end_date (str): Конечная дата периода аналитики.
        telegram_id (int): Идентификатор пользователя Telegram.
        product_id (int, optional): Идентификатор продукта для фильтрации аналитики.

    Возвращает:
        dict или None: Ответ сервера в формате JSON или None при ошибке соединения.
    """
    data = {
        'period_start': start_date,
        'period_end': end_date,
        'telegram_id': telegram_id,
        'product_id': product_id
    }

    return await send_post_request('analytics/get_analytics_data', data)


def generate_sales_chart(analytics_data):
    """
    Генерирует график продаж на основе аналитических данных и возвращает его как изображение.

    Аргументы:
        analytics_data (dict): Данные аналитики продаж.

    Возвращает:
        BytesIO: Буфер изображения с графиком.
    """
    # Агрегируем данные перед построением графика
    aggregated_data = aggregate_sales_data(analytics_data.get('data', []))
    dates = [format_date(data['period_start']) for data in aggregated_data]
    revenue = [float(data['total_revenue']) for data in aggregated_data]

    # Построение столбчатой диаграммы с датами и выручкой
    plt.figure(figsize=(14, 6))
    plt.bar(dates, revenue, color='lightblue', label='Выручка')

    plt.xlabel('Дата')
    plt.ylabel('Выручка (руб.)')
    plt.title('Аналитика продаж')
    plt.legend()
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=8))  # Ограничение количества меток по оси X
    plt.tight_layout()

    # Сохранение графика в буфер памяти
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()  # Закрытие графика для освобождения памяти
    return buffer


def aggregate_sales_data(data):
    """
    Агрегирует данные аналитики по дням для каждого продукта.

    Аргументы:
        data (list): Список данных аналитики с полями 'period_start', 'total_sales' и 'total_revenue'.

    Возвращает:
        list: Отсортированный список агрегированных данных.
    """
    aggregated_data = {}
    for record in data:
        date = record['period_start']
        total_sales = int(record['total_sales'])
        total_revenue = float(record['total_revenue'])

        if date in aggregated_data:
            # Увеличиваем количество продаж и выручку для уже существующей даты
            aggregated_data[date]['total_sales'] += total_sales
            aggregated_data[date]['total_revenue'] += total_revenue
        else:
            # Создаем запись для новой даты
            aggregated_data[date] = {'total_sales': total_sales, 'total_revenue': total_revenue}

    # Преобразуем и сортируем агрегированные данные по дате
    sorted_data = sorted(
        [{'period_start': k, 'total_sales': v['total_sales'], 'total_revenue': v['total_revenue']} for k, v in aggregated_data.items()],
        key=lambda x: x['period_start']
    )
    return sorted_data


def format_date(date_str):
    """
    Форматирует строку даты из формата 'YYYY-MM-DD' в 'DD.MM.YYYY'.

    Аргументы:
        date_str (str): Строка даты в формате 'YYYY-MM-DD'.

    Возвращает:
        str: Отформатированная строка даты в формате 'DD.MM.YYYY'.
    """
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%d.%m.%Y')


def get_dates_by_period(period: str):
    """
    Возвращает начальную и конечную даты для заданного периода времени.

    Аргументы:
        period (str): Период времени (например, 'Год', 'Месяц').

    Возвращает:
        tuple: Начальная и конечная даты в формате 'YYYY-MM-DD'.
    """
    from datetime import datetime, timedelta

    end_date = datetime.today()  # Текущая дата
    if period == "За все время":
        start_date = datetime(2020, 1, 1)  # Начальная дата с начала 2020 года
    elif period == "Год":
        start_date = end_date - timedelta(days=365)
    elif period == "6 месяцев":
        start_date = end_date - timedelta(days=182)
    elif period == "3 месяца":
        start_date = end_date - timedelta(days=91)
    elif period == "Месяц":
        start_date = end_date - timedelta(days=30)
    elif period == "2 недели":
        start_date = end_date - timedelta(days=14)
    elif period == "Неделя":
        start_date = end_date - timedelta(days=7)
    elif period == "День":
        start_date = end_date - timedelta(days=1)
    else:
        start_date = end_date  # Если период не распознан, возвращаем только текущую дату

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
