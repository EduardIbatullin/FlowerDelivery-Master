# flowerdelivery/tests/test_urls.py

from django.test import SimpleTestCase  # Импорт базового класса для простого тестирования
from django.urls import reverse, resolve  # Импорт функций для работы с URL и их разрешением

from apps.users.views import save_telegram_id  # Импорт представления для сохранения Telegram ID
from apps.analytics.views import get_analytics_data  # Импорт представления для получения аналитических данных
from flowerdelivery.views import home_view  # Импорт представления главной страницы


class FlowerDeliveryURLTests(SimpleTestCase):
    """
    Тестовый класс для проверки основных URL-адресов проекта flowerdelivery.

    Включает тесты для проверки маршрутов и соответствующих представлений для
    всех основных приложений проекта, таких как главная страница, админка,
    аналитика, корзина, каталог, пользователи, отзывы, управление и заказы.
    """

    def test_home_url(self):
        """
        Проверка URL-адреса главной страницы.

        Убеждается, что URL-адрес '/' правильно разрешается в представление home_view.
        """
        url = reverse('home')  # Получаем URL по имени маршрута
        self.assertEqual(resolve(url).func, home_view)  # Проверяем, что разрешение URL приводит к ожидаемому представлению

    def test_admin_url(self):
        """
        Проверка URL-адреса административной панели.

        Убеждается, что URL-адрес '/admin/' разрешается в административную панель.
        Также проверяет пространство имен и имя представления.
        """
        url = reverse('admin:index')  # Получаем URL для административной панели
        resolved_view = resolve(url)  # Разрешаем URL в представление
        self.assertEqual(resolved_view.namespace, 'admin')  # Проверяем пространство имен
        self.assertEqual(resolved_view.view_name, 'admin:index')  # Проверяем имя представления

    def test_analytics_urls(self):
        """
        Проверка URL-адресов приложения analytics.

        Убеждается, что URL-адреса 'analytics/analytics_dashboard', 'analytics/update_analytics'
        и 'analytics/get_analytics_data' правильно разрешаются в соответствующие представления.
        """
        url = reverse('analytics:analytics_dashboard')  # Получаем URL для панели аналитики
        resolved_view = resolve(url)  # Разрешаем URL в представление
        self.assertEqual(resolved_view.namespace, 'analytics')  # Проверяем пространство имен
        self.assertEqual(resolved_view.view_name, 'analytics:analytics_dashboard')  # Проверяем имя представления

        url = reverse('analytics:update_analytics')  # Получаем URL для обновления аналитики
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'analytics')
        self.assertEqual(resolved_view.view_name, 'analytics:update_analytics')

        url = reverse('analytics:get_analytics_data')  # Получаем URL для получения аналитических данных
        self.assertEqual(resolve(url).func, get_analytics_data)  # Проверяем, что URL ведет на нужное представление

    def test_cart_urls(self):
        """
        Проверка URL-адресов приложения cart.

        Убеждается, что URL-адрес 'cart/cart_detail' правильно разрешается в представление cart_detail.
        """
        url = reverse('cart:cart_detail')  # Получаем URL для детальной страницы корзины
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'cart')  # Проверяем пространство имен
        self.assertEqual(resolved_view.view_name, 'cart:cart_detail')  # Проверяем имя представления

    def test_catalog_urls(self):
        """
        Проверка URL-адресов приложения catalog.

        Убеждается, что URL-адрес 'catalog/catalog_list' правильно разрешается в представление catalog_list.
        """
        url = reverse('catalog:catalog_list')  # Получаем URL для страницы списка каталога
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'catalog')
        self.assertEqual(resolved_view.view_name, 'catalog:catalog_list')

    def test_users_urls(self):
        """
        Проверка URL-адресов приложения users.

        Убеждается, что URL-адреса 'users/profile' и 'users/save_telegram_id' правильно
        разрешаются в соответствующие представления.
        """
        url = reverse('users:profile')  # Получаем URL для страницы профиля
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'users')
        self.assertEqual(resolved_view.view_name, 'users:profile')

        url = reverse('users:save_telegram_id')  # Получаем URL для сохранения Telegram ID
        self.assertEqual(resolve(url).func, save_telegram_id)  # Проверяем, что URL ведет на нужное представление

    def test_reviews_urls(self):
        """
        Проверка URL-адресов приложения reviews.

        Убеждается, что URL-адрес 'reviews/add_review/<int:product_id>' правильно разрешается
        в представление add_review.
        """
        url = reverse('reviews:add_review', args=[1])  # Получаем URL для добавления отзыва
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'reviews')
        self.assertEqual(resolved_view.view_name, 'reviews:add_review')

    def test_management_urls(self):
        """
        Проверка URL-адресов приложения management.

        Убеждается, что URL-адрес 'management/order_list' правильно разрешается в представление order_list.
        """
        url = reverse('management:order_list')  # Получаем URL для списка заказов
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'management')
        self.assertEqual(resolved_view.view_name, 'management:order_list')

    def test_orders_urls(self):
        """
        Проверка URL-адресов приложения orders.

        Убеждается, что URL-адрес 'orders/order_create' правильно разрешается в представление order_create.
        """
        url = reverse('orders:order_create')  # Получаем URL для создания заказа
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'orders')
        self.assertEqual(resolved_view.view_name, 'orders:order_create')
