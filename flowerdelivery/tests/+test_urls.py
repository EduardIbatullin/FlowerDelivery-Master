# flowerdelivery/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.users.views import save_telegram_id
from apps.analytics.views import get_analytics_data
from flowerdelivery.views import home_view

class FlowerDeliveryURLTests(SimpleTestCase):
    """Тесты для проверки основных URL-адресов проекта flowerdelivery"""

    def test_home_url(self):
        """Тест главной страницы"""
        url = reverse('home')
        self.assertEqual(resolve(url).func, home_view)

    def test_admin_url(self):
        """Тест URL-адреса административной панели"""
        url = reverse('admin:index')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'admin')
        self.assertEqual(resolved_view.view_name, 'admin:index')  # Исправлено: добавлено пространство имён

    def test_analytics_urls(self):
        """Тест URL-адресов приложения analytics"""
        url = reverse('analytics:analytics_dashboard')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'analytics')
        self.assertEqual(resolved_view.view_name, 'analytics:analytics_dashboard')  # Исправлено

        url = reverse('analytics:update_analytics')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'analytics')
        self.assertEqual(resolved_view.view_name, 'analytics:update_analytics')  # Исправлено

        url = reverse('analytics:get_analytics_data')
        self.assertEqual(resolve(url).func, get_analytics_data)

    def test_cart_urls(self):
        """Тест URL-адресов приложения cart"""
        url = reverse('cart:cart_detail')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'cart')
        self.assertEqual(resolved_view.view_name, 'cart:cart_detail')  # Исправлено

    def test_catalog_urls(self):
        """Тест URL-адресов приложения catalog"""
        url = reverse('catalog:catalog_list')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'catalog')
        self.assertEqual(resolved_view.view_name, 'catalog:catalog_list')  # Исправлено

    def test_users_urls(self):
        """Тест URL-адресов приложения users"""
        url = reverse('users:profile')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'users')
        self.assertEqual(resolved_view.view_name, 'users:profile')  # Исправлено

        url = reverse('users:save_telegram_id')
        self.assertEqual(resolve(url).func, save_telegram_id)

    def test_reviews_urls(self):
        """Тест URL-адресов приложения reviews"""
        url = reverse('reviews:add_review', args=[1])
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'reviews')
        self.assertEqual(resolved_view.view_name, 'reviews:add_review')  # Исправлено

    def test_management_urls(self):
        """Тест URL-адресов приложения management"""
        url = reverse('management:order_list')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'management')
        self.assertEqual(resolved_view.view_name, 'management:order_list')  # Исправлено

    def test_orders_urls(self):
        """Тест URL-адресов приложения orders"""
        url = reverse('orders:order_create')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.namespace, 'orders')
        self.assertEqual(resolved_view.view_name, 'orders:order_create')  # Исправлено

