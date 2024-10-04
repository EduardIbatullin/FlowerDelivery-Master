# apps/analytics/utils.py

from apps.orders.models import Order  # Импорт модели для работы с завершенными заказами
from .models import SalesAnalytics  # Импорт модели для сохранения аналитических данных


def update_analytics_data():
    """
    Функция для обновления аналитических данных по продажам.

    Удаляет все текущие записи аналитики и создает новые на основе завершенных заказов.
    Собирает информацию о количестве продаж и общей выручке для каждого продукта на основе завершенных заказов.

    Процесс работы:
    1. Удаляются все старые записи из модели `SalesAnalytics`.
    2. Извлекаются все завершенные заказы (с фильтром `status='Доставлен'`).
    3. Для каждого заказа собираются данные о проданных продуктах, количестве и общей выручке.
    4. Для каждого продукта создаются новые записи аналитики в таблице `SalesAnalytics`.

    Примечание:
        - Убедитесь, что статус заказов в фильтре `Order.objects.filter(status='Доставлен')`
          соответствует фактическому статусу завершенных заказов в проекте.

    Возвращает:
        None: Функция выполняет операции с базой данных и не возвращает значение.
    """
    # Удаление всех старых записей аналитики
    SalesAnalytics.objects.all().delete()

    # Извлечение всех завершенных заказов для анализа
    orders = Order.objects.filter(status='Доставлен')

    product_sales_data = {}  # Словарь для накопления данных по продажам

    # Обработка данных каждого заказа и добавление информации о продажах
    for order in orders:
        for item in order.items.all():
            product = item.product
            order_date = order.delivery_date

            # Инициализация данных для продукта, если он еще не добавлен в словарь
            if product not in product_sales_data:
                product_sales_data[product] = []

            # Сохранение данных о продажах для текущего продукта
            product_sales_data[product].append({
                'total_sales': item.quantity,
                'total_revenue': item.quantity * item.product.price,
                'order_date': order_date,
            })

    # Создание новых записей аналитики в базе данных
    for product, sales_data in product_sales_data.items():
        for sale in sales_data:
            SalesAnalytics.objects.create(
                product=product,
                total_sales=sale['total_sales'],
                total_revenue=sale['total_revenue'],
                period_start=sale['order_date'],
                period_end=sale['order_date'],
            )
