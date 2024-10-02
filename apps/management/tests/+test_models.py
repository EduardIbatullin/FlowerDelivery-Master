# apps/management/tests/test_models.py

from django.test import TestCase
from apps.management.models import OrderStatusHistory
from apps.orders.models import Order
from apps.users.models import CustomUser  # Используем кастомную модель пользователя
from django.utils import timezone


class OrderStatusHistoryModelTest(TestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

        # Создание тестового заказа
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Тестовый адрес',
            contact_phone='1234567890',
            status='В ожидании',
            complete=False
        )

        # Создание записи истории изменения статуса
        self.status_history = OrderStatusHistory.objects.create(
            order=self.order,
            previous_status='В ожидании',
            new_status='В обработке',
            changed_by=self.user,
            changed_at=timezone.now()
        )

    def test_order_status_history_creation(self):
        """Проверка корректности создания записи истории изменения статуса."""
        self.assertEqual(self.status_history.order, self.order)
        self.assertEqual(self.status_history.previous_status, 'В ожидании')
        self.assertEqual(self.status_history.new_status, 'В обработке')
        self.assertEqual(self.status_history.changed_by, self.user)

    def test_order_status_history_str(self):
        """Проверка строкового представления модели OrderStatusHistory."""
        expected_str = f"Заказ #{self.order.id}: В ожидании → В обработке (Изменено: {self.user})"
        self.assertEqual(str(self.status_history), expected_str)
