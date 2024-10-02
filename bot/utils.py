# bot/utils.py

import aiohttp
import matplotlib.pyplot as plt
from io import BytesIO
from config import DJANGO_SERVER_URL, TELEGRAM_BOT_TOKEN
from datetime import datetime

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


async def send_telegram_message(chat_id, text):
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
    url = f"{DJANGO_SERVER_URL}/{endpoint}/"
    headers = {'Content-Type': 'application/json; charset=utf-8'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers, timeout=10) as response:
                if response.status != 200:
                    return None
                return await response.json()
    except aiohttp.ClientError as e:
        return None


async def get_sales_analytics(start_date, end_date, telegram_id, product_id=None):
    data = {
        'period_start': start_date,
        'period_end': end_date,
        'telegram_id': telegram_id,
        'product_id': product_id
    }

    return await send_post_request('analytics/get_analytics_data', data)


def generate_sales_chart(analytics_data):
    aggregated_data = aggregate_sales_data(analytics_data.get('data', []))
    dates = [format_date(data['period_start']) for data in aggregated_data]
    revenue = [float(data['total_revenue']) for data in aggregated_data]

    plt.figure(figsize=(14, 6))
    plt.bar(dates, revenue, color='lightblue', label='Выручка')

    plt.xlabel('Дата')
    plt.ylabel('Выручка (руб.)')
    plt.title('Аналитика продаж')
    plt.legend()
    plt.xticks(rotation=45, ha='right', fontsize=8)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(nbins=8))  # Ограничение количества меток по оси X
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer


def aggregate_sales_data(data):
    aggregated_data = {}
    for record in data:
        date = record['period_start']
        total_sales = int(record['total_sales'])
        total_revenue = float(record['total_revenue'])

        if date in aggregated_data:
            aggregated_data[date]['total_sales'] += total_sales
            aggregated_data[date]['total_revenue'] += total_revenue
        else:
            aggregated_data[date] = {'total_sales': total_sales, 'total_revenue': total_revenue}

    sorted_data = sorted(
        [{'period_start': k, 'total_sales': v['total_sales'], 'total_revenue': v['total_revenue']} for k, v in aggregated_data.items()],
        key=lambda x: x['period_start']
    )
    return sorted_data


def format_date(date_str):
    date = datetime.strptime(date_str, '%Y-%m-%d')
    return date.strftime('%d.%m.%Y')


def get_dates_by_period(period: str):
    from datetime import datetime, timedelta

    end_date = datetime.today()
    if period == "За все время":
        start_date = datetime(2020, 1, 1)
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
        start_date = end_date

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")
