# apps/management/tests/test_views.py

from django.test import TestCase, Client  # Импорты для работы с тестами и клиентом
from django.urls import reverse  # Импорт для построения URL на основе имени маршрута

from apps.orders.models import Order  # Импорт модели заказа для тестирования представлений
from apps.users.models import CustomUser  # Импорт кастомной модели пользователя для управления правами доступа


class ManagementViewsTest(TestCase):
    """
    Набор тестов для проверки представлений приложения управления заказами (management).

    Включает тесты на проверку доступа к списку заказов, истории изменения статусов, деталей заказа,
    а также изменение статуса заказа для администратора. Дополнительно проверяется доступ для обычных пользователей.
    """

    def setUp(self):
        """
        Метод инициализации данных перед запуском тестов.

        Создает тестового пользователя-администратора, обычного пользователя и тестовый заказ.
        Аутентифицирует тестового клиента под учетной записью администратора.
        """
        # Создаем тестового администратора и обычного пользователя
        self.admin_user = CustomUser.objects.create_user(username='adminuser', password='adminpassword')
        self.admin_user.is_staff = True  # Назначаем пользователю права администратора
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
        """
        Тестирование доступа к списку заказов для администратора.

        Проверяет, что страница списка заказов доступна для администратора
        и возвращает корректный HTTP-статус 200.
        """
        response = self.client.get(reverse('management:order_list'))  # Получение URL для списка заказов
        self.assertEqual(response.status_code, 200)  # Проверка HTTP-статуса

    def test_order_detail_view(self):
        """
        Тестирование доступа к деталям заказа для администратора.

        Проверяет, что страница с детальной информацией о заказе доступна для администратора,
        отображает корректные данные заказа и возвращает HTTP-статус 200.
        """
        url = reverse('management:order_detail', args=[self.order.id])  # Получение URL для детальной информации о заказе
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка HTTP-статуса
        self.assertContains(response, f'Детали заказа #{self.order.id}')  # Проверка наличия заголовка с ID заказа

    def test_order_status_history_view(self):
        """
        Тестирование доступа к истории статусов заказа для администратора.

        Проверяет, что страница с историей изменений статуса заказа доступна для администратора,
        отображает корректные данные и возвращает HTTP-статус 200.
        """
        url = reverse('management:order_status_history', args=[self.order.id])  # Получение URL для истории статусов заказа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка HTTP-статуса
        self.assertContains(response, 'История изменений статуса')  # Проверка наличия заголовка истории статусов

    def test_change_order_status_view_get(self):
        """
        Тестирование GET-запроса к изменению статуса заказа для администратора.

        Проверяет, что страница изменения статуса заказа доступна для администратора,
        отображает форму изменения статуса и возвращает HTTP-статус 200.
        """
        url = reverse('management:change_order_status', args=[self.order.id])  # Получение URL для изменения статуса заказа
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка HTTP-статуса
        self.assertContains(response, 'Изменение статуса заказа')  # Проверка наличия заголовка

    def test_change_order_status_view_post(self):
        """
        Тестирование изменения статуса заказа через POST-запрос.

        Выполняет POST-запрос для изменения статуса заказа и проверяет,
        что статус заказа обновляется в базе данных и возвращается корректный HTTP-статус 200.
        """
        url = reverse('management:change_order_status', args=[self.order.id])  # Получение URL для изменения статуса заказа

        # Изменение статуса заказа через POST-запрос
        response = self.client.post(url, {'status': 'Доставлен', 'change_status': True}, follow=True)  # Следуем за редиректом
        self.order.refresh_from_db()  # Обновляем объект заказа для проверки изменений

        self.assertEqual(response.status_code, 200)  # Проверка HTTP-статуса
        self.assertEqual(self.order.status, 'Доставлен')  # Проверка, что статус изменился

    def test_access_control_for_non_admin(self):
        """
        Тестирование ограничения доступа к представлениям для обычного пользователя.

        Выполняет проверку, что обычный пользователь не имеет доступа к представлениям управления заказами
        и перенаправляется на страницу каталога.
        """
        # Логаут текущего администратора и логин обычного пользователя
        self.client.logout()  # Выход из учетной записи администратора
        self.client.login(username='testuser', password='testpassword')  # Вход под учетной записью обычного пользователя

        # Проверка доступа к представлениям управления заказами
        response = self.client.get(reverse('management:order_list'), follow=True)  # Следуем за редиректом

        # Проверка, что в цепочке редиректов есть переход на страницу каталога
        expected_redirect_url = reverse('catalog:catalog_list')  # Используем URL из маршрутов каталога
        self.assertRedirects(response, expected_redirect_url, status_code=302, target_status_code=200)  # Проверка редиректа
