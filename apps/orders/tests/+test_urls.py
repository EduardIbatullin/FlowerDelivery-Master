# apps/orders/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.orders.views import (
    order_create_view,
    order_history_view,
    cart_detail_view,
    order_summary_view,
    order_success_view,
    update_cart_view,
    delete_item_view,
    update_order_item
)
from apps.users.views import profile_view


class OrdersURLsTest(SimpleTestCase):
    def test_order_create_url_resolves(self):
        """Тест разрешения URL для создания заказа."""
        url = reverse('orders:order_create')
        self.assertEqual(resolve(url).func, order_create_view)

    def test_order_history_url_resolves(self):
        """Тест разрешения URL для истории заказов."""
        url = reverse('orders:order_history')
        self.assertEqual(resolve(url).func, order_history_view)

    def test_cart_detail_url_resolves(self):
        """Тест разрешения URL для страницы корзины."""
        url = reverse('orders:cart_detail')
        self.assertEqual(resolve(url).func, cart_detail_view)

    def test_order_summary_url_resolves(self):
        """Тест разрешения URL для подтверждения заказа."""
        url = reverse('orders:order_summary')
        self.assertEqual(resolve(url).func, order_summary_view)

    def test_order_success_url_resolves(self):
        """Тест разрешения URL для успешного завершения заказа."""
        url = reverse('orders:order_success')
        self.assertEqual(resolve(url).func, order_success_view)

    def test_update_cart_url_resolves(self):
        """Тест разрешения URL для обновления корзины."""
        url = reverse('orders:update_cart')
        self.assertEqual(resolve(url).func, update_cart_view)

    def test_delete_item_url_resolves(self):
        """Тест разрешения URL для удаления товаров из корзины."""
        url = reverse('orders:delete_item', args=[1])
        self.assertEqual(resolve(url).func, delete_item_view)

    def test_profile_url_resolves(self):
        """Тест разрешения URL для профиля пользователя."""
        url = reverse('orders:profile')
        self.assertEqual(resolve(url).func, profile_view)

    def test_update_order_item_url_resolves(self):
        """Тест разрешения URL для обновления количества букетов."""
        url = reverse('orders:update_order_item', args=[1])
        self.assertEqual(resolve(url).func, update_order_item)
