# apps/management/tests/test_urls.py

from django.test import TestCase, Client  # Импорты для тестирования представлений и клиентского взаимодействия
from django.urls import reverse  # Функция для получения URL по имени маршрута

from apps.orders.models import Order  # Импорт модели Order для работы с заказами
from apps.users.models import CustomUser  # Кастомная модель пользователя для тестирования прав доступа


class ManagementURLsTest(TestCase):
    """
    Набор тестов для проверки доступности URL-адресов, используемых в приложении управления заказами.

    Включает тесты на проверку доступности страниц списка заказов, изменения статуса заказа,
    просмотра истории изменения статуса, а также страницы с детальной информацией о заказе.
    """

    def setUp(self):
        """
        Метод инициализации данных перед запуском тестов.

        Создает тестового пользователя с правами администратора и выполняет его аутентификацию
        в клиенте. Создается тестовый заказ, который используется в тестах для проверки URL-адресов.
        """
        # Создание тестового администратора и его аутентификация
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.user.is_staff = True  # Назначаем пользователю права администратора
        self.user.save()

        # Инициализация тестового клиента и вход под учетной записью администратора
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Создание тестового заказа, который будет использоваться в тестах
        self.order = Order.objects.create(
            user=self.user,
            status='В ожидании',
            delivery_address='Тестовый адрес',
            contact_phone='1234567890'
        )

    def test_order_list_url(self):
        """
        Тестирование доступности URL-адреса для списка заказов.

        Проверяет, что страница списка заказов доступна для администратора
        и возвращает корректный HTTP-статус 200.
        """
        response = self.client.get(reverse('management:order_list'))  # Получение URL для списка заказов
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")

    def test_order_status_change_url(self):
        """
        Тестирование доступности URL-адреса для изменения статуса заказа.

        Проверяет, что страница изменения статуса заказа доступна для администратора
        и возвращает корректный HTTP-статус 200.
        """
        url = reverse('management:change_order_status', args=[self.order.id])  # Получение URL для изменения статуса заказа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")

    def test_order_status_history_url(self):
        """
        Тестирование доступности URL-адреса для просмотра истории изменений статуса заказа.

        Проверяет, что страница с историей изменений статуса заказа доступна для администратора
        и возвращает корректный HTTP-статус 200.
        """
        url = reverse('management:order_status_history', args=[self.order.id])  # Получение URL для истории статусов заказа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")

    def test_order_detail_url(self):
        """
        Тестирование доступности URL-адреса для просмотра деталей заказа.

        Проверяет, что страница с детальной информацией о заказе доступна для администратора
        и возвращает корректный HTTP-статус 200.
        """
        url = reverse('management:order_detail', args=[self.order.id])  # Получение URL для детальной информации о заказе
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, f"Expected status code 200 but got {response.status_code}. URL may require different permissions or login.")
