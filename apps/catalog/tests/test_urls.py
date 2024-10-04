# apps/catalog/tests/test_urls.py

from django.test import SimpleTestCase  # Импорт базового класса тестов для проверки URL-маршрутов
from django.urls import resolve, reverse  # Импорт функций для формирования и разрешения URL

from apps.catalog.views import catalog_list_view, product_detail_view  # Импорт представлений каталога для проверки URL


class CatalogUrlsTest(SimpleTestCase):
    """
    Тесты для проверки URL-маршрутов приложения каталога.

    Тестируемые сценарии:
    1. Проверка правильности разрешения URL для списка товаров.
    2. Проверка правильности разрешения URL для страницы детального описания продукта.
    """

    def test_catalog_list_url(self):
        """
        Проверка URL для списка товаров.

        Убеждается, что URL 'catalog:catalog_list' правильно разрешается
        и связан с функцией представления `catalog_list_view`.
        """
        url = reverse('catalog:catalog_list')  # Генерация URL для списка товаров
        self.assertEqual(resolve(url).func, catalog_list_view)  # Проверка соответствия представления

    def test_product_detail_url(self):
        """
        Проверка URL для страницы детального описания продукта.

        Убеждается, что URL 'catalog:product_detail' правильно разрешается
        и связан с функцией представления `product_detail_view`.
        """
        url = reverse('catalog:product_detail', args=[1])  # Генерация URL для продукта с id=1
        self.assertEqual(resolve(url).func, product_detail_view)  # Проверка соответствия представления
