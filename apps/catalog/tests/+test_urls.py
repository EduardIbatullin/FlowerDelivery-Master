# apps/catalog/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.catalog.views import catalog_list_view, product_detail_view


class CatalogUrlsTest(SimpleTestCase):
    def test_catalog_list_url(self):
        """Проверка URL для списка товаров"""
        url = reverse('catalog:catalog_list')
        self.assertEqual(resolve(url).func, catalog_list_view)

    def test_product_detail_url(self):
        """Проверка URL для страницы детального описания продукта"""
        url = reverse('catalog:product_detail', args=[1])  # Продукт с id=1
        self.assertEqual(resolve(url).func, product_detail_view)
