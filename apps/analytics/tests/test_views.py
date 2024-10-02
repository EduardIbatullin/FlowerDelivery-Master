# apps/analytics/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.analytics.models import SalesAnalytics
from apps.orders.models import Order, OrderItem
from apps.users.models import Profile
from django.utils import timezone
import json

User = get_user_model()


class AnalyticsViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем пользователей и их профили
        cls.admin_user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        cls.regular_user = User.objects.create_user(username='user', password='user', email='user@example.com')

        cls.admin_profile, _ = Profile.objects.update_or_create(
            user=cls.admin_user, defaults={'telegram_id': '123456'}
        )
        cls.regular_profile, _ = Profile.objects.update_or_create(
            user=cls.regular_user, defaults={'telegram_id': '654321'}
        )

        # Создаем тестовые продукты и заказы
        cls.product_1 = Product.objects.create(name="Розы красные", price=3000.0, description="Красные розы для любимых", is_available=True)
        cls.product_2 = Product.objects.create(name="Букет с лилиями", price=4500.0, description="Букет с ароматными лилиями", is_available=True)

        cls.order_1 = Order.objects.create(user=cls.admin_user, status='Доставлен', delivery_date=timezone.now().date())
        OrderItem.objects.create(order=cls.order_1, product=cls.product_1, quantity=2, price_at_purchase=cls.product_1.price)
        OrderItem.objects.create(order=cls.order_1, product=cls.product_2, quantity=1, price_at_purchase=cls.product_2.price)

        SalesAnalytics.objects.create(product=cls.product_1, total_sales=2, total_revenue=6000.0, period_start=cls.order_1.delivery_date, period_end=cls.order_1.delivery_date)

        cls.client = Client()

    def test_analytics_dashboard_access(self):
        """Тест доступа к аналитической панели для администратора."""
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('analytics:analytics_dashboard'))  # Используем namespace 'analytics'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analytics/analytics_dashboard.html')
        self.assertContains(response, 'Аналитика и отчеты')  # Проверим наличие заголовка

    def test_update_analytics_view(self):
        """Тест обновления аналитики продаж через интерфейс администратора."""
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('analytics:update_analytics'))  # Проверка с namespace 'analytics'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('analytics:analytics_dashboard'))  # Редирект должен вести на панель аналитики

    def test_get_analytics_data_api(self):
        """Тест API для получения аналитических данных через telegram_id."""
        # Проверка наличия профиля для админа и его корректность
        self.admin_profile.refresh_from_db()
        self.assertEqual(self.admin_profile.telegram_id, '123456')

        # Создаем запрос с корректными данными, включая telegram_id администратора
        data = {
            'period_start': str(self.order_1.delivery_date),
            'period_end': str(self.order_1.delivery_date),
            'product_id': self.product_1.id,
            'telegram_id': self.admin_profile.telegram_id  # Используем telegram_id администратора
        }
        response = self.client.post(reverse('analytics:get_analytics_data'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['total_orders'], 2)
        self.assertEqual(float(response_data['total_revenue']), 6000.0)
        self.assertIn('data', response_data)
        self.assertEqual(len(response_data['data']), 1)

    def test_invalid_access_to_views(self):
        """Тест недоступности аналитических представлений для неавторизованного пользователя."""
        # Проверка доступа без авторизации к аналитическим страницам
        response = self.client.get(reverse('analytics:analytics_dashboard'))
        self.assertEqual(response.status_code, 302)  # Неавторизованный пользователь должен быть перенаправлен на страницу входа
        response = self.client.get(reverse('analytics:update_analytics'))
        self.assertEqual(response.status_code, 302)

        # Попытка отправить запрос к API с недопустимым пользователем (не администратор)
        self.regular_profile.refresh_from_db()
        self.assertEqual(self.regular_profile.telegram_id, '654321')

        data = {
            'period_start': str(self.order_1.delivery_date),
            'period_end': str(self.order_1.delivery_date),
            'product_id': self.product_1.id,
            'telegram_id': self.regular_profile.telegram_id  # Используем telegram_id обычного пользователя
        }
        response = self.client.post(reverse('analytics:get_analytics_data'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)  # API должно возвращать 403 для неавторизованного доступа

    def test_invalid_telegram_id_access(self):
        """Тест недоступности API для некорректного telegram_id."""
        # Убедимся, что у нас есть корректный telegram_id
        self.admin_profile.refresh_from_db()
        self.assertEqual(self.admin_profile.telegram_id, '123456')

        # Создаем запрос с несуществующим telegram_id
        data = {
            'period_start': str(self.order_1.delivery_date),
            'period_end': str(self.order_1.delivery_date),
            'product_id': self.product_1.id,
            'telegram_id': 'invalid_telegram_id'  # Некорректный telegram_id
        }

        # Отправляем запрос и проверяем, что возвращается статус 403 и сообщение об ошибке
        response = self.client.post(reverse('analytics:get_analytics_data'), data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Пользователь не найден.')
