# apps/cart/tests/test_urls.py

from django.test import SimpleTestCase  # Импорт класса SimpleTestCase для тестирования URL-маршрутов без базы данных
from django.urls import resolve, reverse  # Импорт функций для формирования и разрешения URL

from apps.cart import views  # Импорт представлений корзины для проверки соответствия URL


class CartUrlsTest(SimpleTestCase):
    """
    Набор тестов для проверки корректности URL-маршрутов приложения корзины.

    Тестируется разрешение URL на соответствующие представления (views) и проверка
    правильности имен маршрутов для каждого действия (добавление в корзину, удаление, обновление).
    """

    def test_add_to_cart_url(self):
        """
        Тестирование URL для добавления товара в корзину.

        Проверяет, что URL `cart:add_to_cart` корректно разрешается на представление `views.add_to_cart`.
        """
        url = reverse('cart:add_to_cart', args=[1])  # Формирование URL для добавления товара с ID 1
        self.assertEqual(resolve(url).func, views.add_to_cart)  # Проверка соответствия представления

    def test_cart_detail_url(self):
        """
        Тестирование URL для отображения корзины.

        Проверяет, что URL `cart:cart_detail` корректно разрешается на представление `views.cart_detail`.
        """
        url = reverse('cart:cart_detail')  # Формирование URL для отображения корзины
        self.assertEqual(resolve(url).func, views.cart_detail)  # Проверка соответствия представления

    def test_update_cart_item_url(self):
        """
        Тестирование URL для обновления элемента корзины.

        Проверяет, что URL `cart:update_cart_item` корректно разрешается на представление `views.update_cart_item`.
        """
        url = reverse('cart:update_cart_item', args=[1])  # Формирование URL для обновления элемента корзины с ID 1
        self.assertEqual(resolve(url).func, views.update_cart_item)  # Проверка соответствия представления

    def test_remove_from_cart_url(self):
        """
        Тестирование URL для удаления элемента из корзины.

        Проверяет, что URL `cart:remove_from_cart` корректно разрешается на представление `views.remove_from_cart`.
        """
        url = reverse('cart:remove_from_cart', args=[1])  # Формирование URL для удаления элемента корзины с ID 1
        self.assertEqual(resolve(url).func, views.remove_from_cart)  # Проверка соответствия представления

    def test_add_to_cart_from_history_url(self):
        """
        Тестирование URL для добавления товара в корзину из истории заказов.

        Проверяет, что URL `cart:add_to_cart_from_history` корректно разрешается на представление `views.add_to_cart_from_history`.
        """
        url = reverse('cart:add_to_cart_from_history', args=[1])  # Формирование URL для добавления товара из истории с ID 1
        self.assertEqual(resolve(url).func, views.add_to_cart_from_history)  # Проверка соответствия представления
