# apps/analytics/tests/test_urls.py

from django.test import SimpleTestCase  # Импортируем SimpleTestCase для создания тестов без обращения к базе данных
from django.urls import reverse, resolve  # Импортируем reverse и resolve для проверки URL-маршрутов

from apps.analytics.views import (  # Импорт представлений для проверки соответствия URL-маршрутов функциям представлений
    analytics_dashboard,
    update_analytics,
    get_analytics_data,
)


class AnalyticsUrlsTest(SimpleTestCase):
    """
    Набор тестов для проверки корректности URL-маршрутов приложения аналитики.

    Проверяет, что каждый URL-маршрут приложения `analytics` корректно разрешается
    на соответствующую функцию представления (view).
    """

    def test_analytics_dashboard_url_resolves(self):
        """
        Тест для проверки разрешения URL аналитической панели.

        Проверяет, что URL-маршрут с именем `analytics_dashboard` корректно разрешается на
        функцию представления `analytics_dashboard`.
        """
        url = reverse('analytics:analytics_dashboard')  # Генерация URL для аналитической панели
        self.assertEqual(resolve(url).func, analytics_dashboard)  # Проверка соответствия представления

    def test_update_analytics_url_resolves(self):
        """
        Тест для проверки разрешения URL обновления аналитики.

        Проверяет, что URL-маршрут с именем `update_analytics` корректно разрешается на
        функцию представления `update_analytics`.
        """
        url = reverse('analytics:update_analytics')  # Генерация URL для обновления аналитики
        self.assertEqual(resolve(url).func, update_analytics)  # Проверка соответствия представления

    def test_get_analytics_data_url_resolves(self):
        """
        Тест для проверки разрешения API URL получения аналитических данных.

        Проверяет, что URL-маршрут с именем `get_analytics_data` корректно разрешается на
        функцию представления `get_analytics_data`.
        """
        url = reverse('analytics:get_analytics_data')  # Генерация URL для получения аналитических данных
        self.assertEqual(resolve(url).func, get_analytics_data)  # Проверка соответствия представления
