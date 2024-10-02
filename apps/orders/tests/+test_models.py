# apps/orders/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product
from datetime import date, time


class OrderModelTest(TestCase):

    def setUp(self):
        # Создаем тестового пользователя
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name='Тестовый продукт',
            price=100.00,
            description='Описание тестового продукта',
            is_available=True
        )

        # Создаем тестовый заказ
        self.order = Order.objects.create(
            user=self.user,
            status='В ожидании',
            total_price=0,  # Изначально общая стоимость равна 0
            delivery_address='Тестовый адрес',
            contact_phone='1234567890',
            delivery_date=date.today(),
            delivery_time=time(14, 30),
            additional_info='Тестовая информация',
            email_notifications=True,
            telegram_notifications=False
        )

        # Создаем элемент заказа
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_purchase=self.product.price
        )

    def test_order_str_representation(self):
        """Проверка строкового представления заказа."""
        self.assertEqual(str(self.order), f"Order {self.order.id} by {self.order.user}")

    def test_order_item_str_representation(self):
        """Проверка строкового представления элемента заказа."""
        self.assertEqual(str(self.order_item), f"2 x Тестовый продукт для заказа {self.order.id}")

    def test_order_total_price_calculation(self):
        """Проверка расчета общей стоимости заказа."""
        # Рассчитываем общую стоимость заказа
        total_price = self.order.get_total_price()
        expected_price = self.order_item.quantity * self.order_item.price_at_purchase
        self.assertEqual(total_price, expected_price)

        # Обновляем общую стоимость в заказе и проверяем
        self.order.total_price = total_price
        self.order.save()
        self.assertEqual(self.order.total_price, expected_price)

    def test_order_item_total_price_property(self):
        """Проверка свойства `total_price` для элемента заказа."""
        total_price = self.order_item.total_price
        self.assertEqual(total_price, self.order_item.quantity * self.order_item.price_at_purchase)

    def test_order_complete_status(self):
        """Проверка статуса завершения заказа."""
        self.assertFalse(self.order.complete)  # Изначально заказ не завершен

        # Завершаем заказ и проверяем статус
        self.order.complete = True
        self.order.save()
        self.assertTrue(self.order.complete)
