# apps/management/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from apps.orders.models import Order
from apps.users.models import CustomUser


class ManagementViewsTest(TestCase):

    def setUp(self):
        # Создаем тестового администратора и обычного пользователя
        self.admin_user = CustomUser.objects.create_user(username='adminuser', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.save()

        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

        # Создаем тестовый заказ для администратора
        self.order = Order.objects.create(
            user=self.admin_user,
            status='В ожидании',
            delivery_address='Тестовый адрес',
            contact_phone='1234567890'
        )

        # Аутентифицируем тестового клиента как администратора
        self.client = Client()
        self.client.login(username='adminuser', password='adminpassword')

    def test_order_list_view(self):
        """Тест доступа к списку заказов для администратора."""
        response = self.client.get(reverse('management:order_list'))
        self.assertEqual(response.status_code, 200)

    def test_order_detail_view(self):
        """Тест доступа к деталям заказа для администратора."""
        url = reverse('management:order_detail', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Детали заказа #{self.order.id}')

    def test_order_status_history_view(self):
        """Тест доступа к истории статусов заказа для администратора."""
        url = reverse('management:order_status_history', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'История изменений статуса')

    def test_change_order_status_view_get(self):
        """Тест GET-запроса к изменению статуса заказа для администратора."""
        url = reverse('management:change_order_status', args=[self.order.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Изменение статуса заказа')

    def test_change_order_status_view_post(self):
        """Тест изменения статуса заказа через POST-запрос."""
        url = reverse('management:change_order_status', args=[self.order.id])

        # Изменение статуса заказа через POST-запрос
        response = self.client.post(url, {'status': 'Доставлен', 'change_status': True}, follow=True)
        self.order.refresh_from_db()  # Обновляем объект заказа

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.order.status, 'Доставлен')  # Проверка, что статус изменился

    def test_access_control_for_non_admin(self):
        """Тест доступа к представлениям для обычного пользователя."""
        # Логаут текущего администратора и логин обычного пользователя
        self.client.logout()
        self.client.login(username='testuser', password='testpassword')

        # Проверка доступа к представлениям управления заказами
        response = self.client.get(reverse('management:order_list'), follow=True)  # Следуем за редиректом

        # Проверка, что в цепочке редиректов есть переход на страницу каталога
        expected_redirect_url = reverse('catalog:catalog_list')  # Используем URL из маршрутов каталога
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)
