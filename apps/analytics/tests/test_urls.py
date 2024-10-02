# apps/analytics/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.analytics.views import analytics_dashboard, update_analytics, get_analytics_data


class AnalyticsUrlsTest(SimpleTestCase):
    def test_analytics_dashboard_url_resolves(self):
        """Тест для проверки разрешения URL аналитической панели."""
        url = reverse('analytics:analytics_dashboard')
        self.assertEqual(resolve(url).func, analytics_dashboard)

    def test_update_analytics_url_resolves(self):
        """Тест для проверки разрешения URL обновления аналитики."""
        url = reverse('analytics:update_analytics')
        self.assertEqual(resolve(url).func, update_analytics)

    def test_get_analytics_data_url_resolves(self):
        """Тест для проверки разрешения API URL получения аналитических данных."""
        url = reverse('analytics:get_analytics_data')
        self.assertEqual(resolve(url).func, get_analytics_data)
