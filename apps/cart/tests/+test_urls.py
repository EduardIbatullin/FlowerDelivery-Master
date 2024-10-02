# apps/cart/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.cart import views


class CartUrlsTest(SimpleTestCase):

    def test_add_to_cart_url(self):
        """Тестирование URL для добавления товара в корзину."""
        url = reverse('cart:add_to_cart', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_cart)

    def test_cart_detail_url(self):
        """Тестирование URL для отображения корзины."""
        url = reverse('cart:cart_detail')
        self.assertEqual(resolve(url).func, views.cart_detail)

    def test_update_cart_item_url(self):
        """Тестирование URL для обновления элемента корзины."""
        url = reverse('cart:update_cart_item', args=[1])
        self.assertEqual(resolve(url).func, views.update_cart_item)

    def test_remove_from_cart_url(self):
        """Тестирование URL для удаления элемента из корзины."""
        url = reverse('cart:remove_from_cart', args=[1])
        self.assertEqual(resolve(url).func, views.remove_from_cart)

    def test_add_to_cart_from_history_url(self):
        """Тестирование URL для добавления товара в корзину из истории заказов."""
        url = reverse('cart:add_to_cart_from_history', args=[1])
        self.assertEqual(resolve(url).func, views.add_to_cart_from_history)
