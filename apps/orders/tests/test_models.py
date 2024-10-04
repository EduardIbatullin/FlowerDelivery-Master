# apps/orders/tests/test_models.py

from datetime import date, time  # Импортируем классы для работы с датами и временем

from django.test import TestCase  # Импортируем базовый класс для создания тестов
from django.contrib.auth import get_user_model  # Импортируем функцию для получения модели пользователя

from apps.orders.models import Order, OrderItem  # Импортируем модели заказа и элементов заказа
from apps.catalog.models import Product  # Импортируем модель продукта для создания тестовых данных


class OrderModelTest(TestCase):
    """
    Набор тестов для проверки модели `Order` и `OrderItem`.

    Проверяет корректность работы моделей, включая создание заказов,
    элементы заказов, вычисление общей стоимости и строковые представления.
    """

    def setUp(self):
        """
        Метод для инициализации тестовых данных перед запуском тестов.

        Создает тестового пользователя, продукт и заказ с элементом заказа для проверки.
        """
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
            price_at_purchase=self.product.price  # Сохраняем цену на момент покупки
        )

    def test_order_str_representation(self):
        """
        Проверка строкового представления заказа.

        Убеждаемся, что метод `__str__` возвращает корректное значение.
        """
        self.assertEqual(str(self.order), f"Order {self.order.id} by {self.order.user}")

    def test_order_item_str_representation(self):
        """
        Проверка строкового представления элемента заказа.

        Убеждаемся, что метод `__str__` возвращает корректное значение.
        """
        self.assertEqual(str(self.order_item), f"{self.order_item.quantity} x {self.product.name} для заказа {self.order.id}")

    def test_order_total_price_calculation(self):
        """
        Проверка расчета общей стоимости заказа.

        Убеждаемся, что метод `get_total_price` корректно вычисляет общую стоимость заказа.
        """
        # Рассчитываем общую стоимость заказа
        total_price = self.order.get_total_price()
        expected_price = self.order_item.quantity * self.order_item.price_at_purchase
        self.assertEqual(total_price, expected_price)

        # Обновляем общую стоимость в заказе и проверяем
        self.order.total_price = total_price
        self.order.save()
        self.assertEqual(self.order.total_price, expected_price)

    def test_order_item_total_price_property(self):
        """
        Проверка свойства `total_price` для элемента заказа.

        Убеждаемся, что оно корректно вычисляет стоимость элемента заказа.
        """
        total_price = self.order_item.total_price
        self.assertEqual(total_price, self.order_item.quantity * self.order_item.price_at_purchase)

    def test_order_complete_status(self):
        """
        Проверка статуса завершения заказа.

        Убеждаемся, что поле `complete` корректно обновляется.
        """
        self.assertFalse(self.order.complete)  # Изначально заказ не завершен

        # Завершаем заказ и проверяем статус
        self.order.complete = True
        self.order.save()
        self.assertTrue(self.order.complete)
