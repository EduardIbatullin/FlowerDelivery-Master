# apps/management/tests/test_urls.py

from django.test import TestCase, Client
from django.urls import reverse
from apps.orders.models import Order
from apps.users.models import CustomUser  # Убедитесь, что используется правильная модель пользователя


class ManagementURLsTest(TestCase):

    def setUp(self):
        # Создаем тестового администратора и аутентифицируем его
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True  # Назначаем пользователю права администратора
        self.user.save()

        # Аутентифицируем тестового клиента
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Создаем тестовый заказ
        self.order = Order.objects.create(
            user=self.user,
            status='В ожидании',
            delivery_address='Тестовый адрес',
            contact_phone='1234567890'
        )

    def test_order_list_url(self):
        """Тест доступности URL-адреса для списка заказов."""
        response = self.client.get(reverse('management:order_list'))
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")

    def test_order_status_change_url(self):
        """Тест доступности URL-адреса для изменения статуса заказа."""
        url = reverse('management:change_order_status', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")

    def test_order_status_history_url(self):
        """Тест доступности URL-адреса для просмотра истории изменений статуса заказа."""
        url = reverse('management:order_status_history', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")

    def test_order_detail_url(self):
        """Тест доступности URL-адреса для просмотра деталей заказа."""
        url = reverse('management:order_detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")
