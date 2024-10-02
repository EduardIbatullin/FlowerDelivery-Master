# apps/analytics/tests/test_utils.py

from django.test import TestCase
from django.utils import timezone
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product
from apps.analytics.models import SalesAnalytics
from apps.analytics.utils import update_analytics_data
from django.contrib.auth import get_user_model

User = get_user_model()

class UpdateAnalyticsDataTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')

        # Создаем тестовые продукты
        cls.product_1 = Product.objects.create(
            name="Розы красные",
            price=3000.0,
            description="Красные розы для любимых",
            is_available=True
        )
        cls.product_2 = Product.objects.create(
            name="Букет с лилиями",
            price=4500.0,
            description="Букет с ароматными лилиями",
            is_available=True
        )

        # Создаем тестовые заказы
        cls.order_1 = Order.objects.create(
            user=cls.user,
            status='Доставлен',
            delivery_date=timezone.now().date()
        )
        cls.order_2 = Order.objects.create(
            user=cls.user,
            status='Доставлен',
            delivery_date=timezone.now().date() - timezone.timedelta(days=1)
        )

        # Добавляем товары в заказы
        OrderItem.objects.create(order=cls.order_1, product=cls.product_1, quantity=2, price_at_purchase=cls.product_1.price)
        OrderItem.objects.create(order=cls.order_1, product=cls.product_2, quantity=1, price_at_purchase=cls.product_2.price)
        OrderItem.objects.create(order=cls.order_2, product=cls.product_1, quantity=3, price_at_purchase=cls.product_1.price)

    def test_update_analytics_data(self):
        """Тест обновления аналитических данных по продажам."""
        # Убедимся, что до вызова функции нет записей в SalesAnalytics
        self.assertEqual(SalesAnalytics.objects.count(), 0)

        # Вызываем функцию обновления аналитики
        update_analytics_data()

        # Убедимся, что записи созданы
        self.assertEqual(SalesAnalytics.objects.count(), 3)

        # Проверка данных по первому продукту
        product_1_analytics = SalesAnalytics.objects.filter(product=self.product_1)
        self.assertEqual(product_1_analytics.count(), 2)

        # Проверка аналитики по первой записи продукта 1 (дата сегодняшнего дня)
        product_1_today = product_1_analytics.get(period_start=timezone.now().date())
        self.assertEqual(product_1_today.total_sales, 2)  # 2 штуки продано сегодня
        self.assertEqual(float(product_1_today.total_revenue), 6000.0)

        # Проверка аналитики по второй записи продукта 1 (дата вчера)
        product_1_yesterday = product_1_analytics.get(period_start=timezone.now().date() - timezone.timedelta(days=1))
        self.assertEqual(product_1_yesterday.total_sales, 3)  # 3 штуки продано вчера
        self.assertEqual(float(product_1_yesterday.total_revenue), 9000.0)

        # Проверка данных по второму продукту
        product_2_analytics = SalesAnalytics.objects.get(product=self.product_2)
        self.assertEqual(product_2_analytics.total_sales, 1)  # 1 штука продано
        self.assertEqual(float(product_2_analytics.total_revenue), 4500.0)

    def test_analytics_data_is_updated_correctly(self):
        """Тест корректного удаления старых записей и создания новых записей."""
        # Создаем старую запись в SalesAnalytics
        SalesAnalytics.objects.create(
            product=self.product_1,
            total_sales=5,
            total_revenue=15000.0,
            period_start=timezone.now().date() - timezone.timedelta(days=10),
            period_end=timezone.now().date() - timezone.timedelta(days=10)
        )

        # Убедимся, что старая запись существует
        self.assertEqual(SalesAnalytics.objects.count(), 1)

        # Вызываем функцию обновления аналитики
        update_analytics_data()

        # Убедимся, что старая запись удалена и созданы новые записи
        self.assertEqual(SalesAnalytics.objects.count(), 3)
        self.assertFalse(SalesAnalytics.objects.filter(period_start=timezone.now().date() - timezone.timedelta(days=10)).exists())
