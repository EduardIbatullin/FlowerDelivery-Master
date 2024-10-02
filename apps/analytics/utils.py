# apps/analytics/utils.py

from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product
from .models import SalesAnalytics
from django.utils import timezone


def update_analytics_data():
    """
    Функция для обновления аналитических данных по продажам.
    """
    # Сначала удаляем старые записи
    SalesAnalytics.objects.all().delete()

    # Получаем все завершенные заказы
    orders = Order.objects.filter(status='Доставлен')  # Убедитесь, что фильтр совпадает с правильным статусом заказов

    # Словарь для накопления данных
    product_sales_data = {}

    # Перебираем заказы и накапливаем данные для каждого продукта
    for order in orders:
        for item in order.items.all():
            product = item.product
            order_date = order.delivery_date

            # Если продукт отсутствует в данных, добавляем его
            if product not in product_sales_data:
                product_sales_data[product] = []

            # Добавляем информацию о продаже с учетом даты
            product_sales_data[product].append({
                'total_sales': item.quantity,
                'total_revenue': item.quantity * item.product.price,
                'order_date': order_date,
            })

    # Создаем новые записи в таблице SalesAnalytics для каждого продукта
    for product, sales_data in product_sales_data.items():
        for sale in sales_data:
            SalesAnalytics.objects.create(
                product=product,
                total_sales=sale['total_sales'],
                total_revenue=sale['total_revenue'],
                period_start=sale['order_date'],
                period_end=sale['order_date'],  # Установим одинаковую дату для начала и конца периода
            )