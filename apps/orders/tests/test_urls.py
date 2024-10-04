# apps/orders/tests/test_urls.py

from django.test import SimpleTestCase  # Импортируем SimpleTestCase для создания тестов без обращения к базе данных
from django.urls import reverse, resolve  # Импортируем reverse и resolve для проверки URL-маршрутов

from apps.orders.views import (  # Импортируем представления для проверки соответствия URL-маршрутов
    order_create_view,
    order_history_view,
    cart_detail_view,
    order_summary_view,
    order_success_view,
    update_cart_view,
    delete_item_view,
    update_order_item
)
from apps.users.views import profile_view  # Импорт представления профиля пользователя


class OrdersURLsTest(SimpleTestCase):
    """
    Набор тестов для проверки корректности URL-маршрутов приложения заказов.

    Проверяет, что каждый URL-маршрут приложения `orders` корректно разрешается
    на соответствующую функцию представления (view).
    """

    def test_order_create_url_resolves(self):
        """
        Тест разрешения URL для создания заказа.

        Проверяет, что URL-маршрут с именем `order_create` корректно разрешается на
        функцию представления `order_create_view`.
        """
        url = reverse('orders:order_create')
        self.assertEqual(resolve(url).func, order_create_view)

    def test_order_history_url_resolves(self):
        """
        Тест разрешения URL для истории заказов.

        Проверяет, что URL-маршрут с именем `order_history` корректно разрешается на
        функцию представления `order_history_view`.
        """
        url = reverse('orders:order_history')
        self.assertEqual(resolve(url).func, order_history_view)

    def test_cart_detail_url_resolves(self):
        """
        Тест разрешения URL для страницы корзины.

        Проверяет, что URL-маршрут с именем `cart_detail` корректно разрешается на
        функцию представления `cart_detail_view`.
        """
        url = reverse('orders:cart_detail')
        self.assertEqual(resolve(url).func, cart_detail_view)

    def test_order_summary_url_resolves(self):
        """
        Тест разрешения URL для подтверждения заказа.

        Проверяет, что URL-маршрут с именем `order_summary` корректно разрешается на
        функцию представления `order_summary_view`.
        """
        url = reverse('orders:order_summary')
        self.assertEqual(resolve(url).func, order_summary_view)

    def test_order_success_url_resolves(self):
        """
        Тест разрешения URL для успешного завершения заказа.

        Проверяет, что URL-маршрут с именем `order_success` корректно разрешается на
        функцию представления `order_success_view`.
        """
        url = reverse('orders:order_success')
        self.assertEqual(resolve(url).func, order_success_view)

    def test_update_cart_url_resolves(self):
        """
        Тест разрешения URL для обновления корзины.

        Проверяет, что URL-маршрут с именем `update_cart` корректно разрешается на
        функцию представления `update_cart_view`.
        """
        url = reverse('orders:update_cart')
        self.assertEqual(resolve(url).func, update_cart_view)

    def test_delete_item_url_resolves(self):
        """
        Тест разрешения URL для удаления товаров из корзины.

        Проверяет, что URL-маршрут с именем `delete_item` корректно разрешается на
        функцию представления `delete_item_view`.
        """
        url = reverse('orders:delete_item', args=[1])
        self.assertEqual(resolve(url).func, delete_item_view)

    def test_profile_url_resolves(self):
        """
        Тест разрешения URL для профиля пользователя.

        Проверяет, что URL-маршрут с именем `profile` корректно разрешается на
        функцию представления `profile_view`.
        """
        url = reverse('orders:profile')
        self.assertEqual(resolve(url).func, profile_view)

    def test_update_order_item_url_resolves(self):
        """
        Тест разрешения URL для обновления количества букетов.

        Проверяет, что URL-маршрут с именем `update_order_item` корректно разрешается на
        функцию представления `update_order_item`.
        """
        url = reverse('orders:update_order_item', args=[1])
        self.assertEqual(resolve(url).func, update_order_item)
