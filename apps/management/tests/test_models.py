# apps/management/tests/test_models.py

from django.test import TestCase  # Импортируем TestCase для создания тестов моделей
from django.utils import timezone  # Импортируем timezone для работы с временными значениями

from apps.management.models import OrderStatusHistory  # Модель для хранения истории изменения статусов заказов
from apps.orders.models import Order  # Модель для хранения данных о заказах
from apps.users.models import CustomUser  # Используем кастомную модель пользователя для управления пользователями


class OrderStatusHistoryModelTest(TestCase):
    """
    Набор тестов для проверки корректности работы модели `OrderStatusHistory`.

    Включает тесты для проверки создания записей об изменении статуса заказа, а также
    правильного отображения строкового представления модели.
    """

    def setUp(self):
        """
        Метод инициализации данных перед каждым тестом.

        Создает тестового пользователя, тестовый заказ, а также одну запись истории
        изменения статуса заказа для последующей проверки.
        """
        # Создание тестового пользователя
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

        # Создание тестового заказа с необходимыми полями
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Тестовый адрес',
            contact_phone='1234567890',
            status='В ожидании',
            complete=False
        )

        # Создание записи истории изменения статуса заказа
        self.status_history = OrderStatusHistory.objects.create(
            order=self.order,
            previous_status='В ожидании',
            new_status='В обработке',
            changed_by=self.user,
            changed_at=timezone.now()  # Устанавливаем текущее время для тестирования
        )

    def test_order_status_history_creation(self):
        """
        Тестирование корректности создания записи истории изменения статуса.

        Проверяет, что все поля записи, включая ссылку на заказ, предыдущий и новый статусы,
        а также пользователя, изменившего статус, сохраняются правильно.
        """
        self.assertEqual(self.status_history.order, self.order)  # Проверяем связь с заказом
        self.assertEqual(self.status_history.previous_status, 'В ожидании')  # Проверяем предыдущий статус
        self.assertEqual(self.status_history.new_status, 'В обработке')  # Проверяем новый статус
        self.assertEqual(self.status_history.changed_by, self.user)  # Проверяем пользователя, изменившего статус

    def test_order_status_history_str(self):
        """
        Тестирование строкового представления модели `OrderStatusHistory`.

        Проверяет, что метод `__str__()` возвращает корректное строковое представление записи
        в формате: "Заказ #{order_id}: {previous_status} → {new_status} (Изменено: {changed_by})".
        """
        expected_str = f"Заказ #{self.order.id}: В ожидании → В обработке (Изменено: {self.user})"  # Ожидаемое строковое представление
        self.assertEqual(str(self.status_history), expected_str)  # Проверяем соответствие строкового представления
