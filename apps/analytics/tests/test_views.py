# apps/analytics/tests/test_views.py

import json  # Импорт модуля для работы с JSON-данными

from django.contrib.auth import get_user_model  # Импорт функции для получения модели пользователя
from django.test import TestCase, Client  # Импорт классов TestCase и Client для создания тестов и имитации запросов
from django.urls import reverse  # Импорт функции для получения URL по имени маршрута
from django.utils import timezone  # Импорт модуля для работы с датами и временем

from apps.analytics.models import SalesAnalytics  # Импорт модели SalesAnalytics для работы с аналитикой продаж
from apps.catalog.models import Product  # Импорт модели Product для работы с продуктами каталога
from apps.orders.models import Order, OrderItem  # Импорт моделей заказа и элементов заказа для работы с заказами
from apps.users.models import Profile  # Импорт модели Profile для работы с профилями пользователей

# Получение модели пользователя
User = get_user_model()


class AnalyticsViewsTest(TestCase):
    """
    Набор тестов для представлений приложения аналитики.

    Включает проверку доступа к панели аналитики, обновление аналитических данных, получение аналитики через API,
    а также проверку недоступности аналитических данных для неавторизованных пользователей или пользователей без прав администратора.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Инициализация тестовых данных перед запуском тестов.

        Создает тестового администратора и обычного пользователя, тестовые профили, продукты (букеты), заказы и
        элементы заказов. Эти данные используются для тестирования представлений аналитики.
        """
        # Создание тестовых пользователей и профилей
        cls.admin_user = User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')
        cls.regular_user = User.objects.create_user(username='user', password='user', email='user@example.com')

        # Создание профилей с telegram_id для тестовых пользователей
        cls.admin_profile, _ = Profile.objects.update_or_create(user=cls.admin_user, defaults={'telegram_id': '123456'})
        cls.regular_profile, _ = Profile.objects.update_or_create(user=cls.regular_user, defaults={'telegram_id': '654321'})

        # Создание тестовых продуктов (букетов)
        cls.product_1 = Product.objects.create(name="Розы красные", price=3000.0, description="Красные розы для любимых", is_available=True)
        cls.product_2 = Product.objects.create(name="Букет с лилиями", price=4500.0, description="Букет с ароматными лилиями", is_available=True)

        # Создание тестового заказа и добавление товаров в заказ
        cls.order_1 = Order.objects.create(user=cls.admin_user, status='Доставлен', delivery_date=timezone.now().date())
        OrderItem.objects.create(order=cls.order_1, product=cls.product_1, quantity=2, price_at_purchase=cls.product_1.price)
        OrderItem.objects.create(order=cls.order_1, product=cls.product_2, quantity=1, price_at_purchase=cls.product_2.price)

        # Создание записи аналитики продаж для тестирования
        SalesAnalytics.objects.create(product=cls.product_1, total_sales=2, total_revenue=6000.0,
                                      period_start=cls.order_1.delivery_date, period_end=cls.order_1.delivery_date)

        # Инициализация клиента для отправки HTTP-запросов в тестах
        cls.client = Client()

    def test_analytics_dashboard_access(self):
        """
        Тест доступа к аналитической панели для администратора.

        Проверяет, что администратор имеет доступ к странице аналитики, а также что страница загружается корректно
        и использует правильный шаблон.
        """
        self.client.login(username='admin', password='admin')  # Авторизация администратора
        response = self.client.get(reverse('analytics:analytics_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'analytics/analytics_dashboard.html')
        self.assertContains(response, 'Аналитика и отчеты')  # Проверка наличия заголовка на странице

    def test_update_analytics_view(self):
        """
        Тест обновления аналитики продаж через интерфейс администратора.

        Проверяет, что администратор может выполнить обновление аналитики и что после обновления
        происходит корректное перенаправление на панель аналитики.
        """
        self.client.login(username='admin', password='admin')  # Авторизация администратора
        response = self.client.get(reverse('analytics:update_analytics'))
        self.assertEqual(response.status_code, 302)  # Ожидается перенаправление (status code 302)
        self.assertRedirects(response, reverse('analytics:analytics_dashboard'))  # Редирект на панель аналитики

    def test_get_analytics_data_api(self):
        """
        Тест API для получения аналитических данных через telegram_id.

        Проверяет, что администратор, имеющий валидный `telegram_id`, может получать данные аналитики
        через API и что возвращенные данные корректны.
        """
        # Обновляем профиль и проверяем его корректность
        self.admin_profile.refresh_from_db()
        self.assertEqual(self.admin_profile.telegram_id, '123456')

        # Отправка POST-запроса с корректными данными
        data = {
            'period_start': str(self.order_1.delivery_date),
            'period_end': str(self.order_1.delivery_date),
            'product_id': self.product_1.id,
            'telegram_id': self.admin_profile.telegram_id
        }
        response = self.client.post(reverse('analytics:get_analytics_data'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # Проверка возвращенных данных
        response_data = response.json()
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['total_orders'], 2)
        self.assertEqual(float(response_data['total_revenue']), 6000.0)
        self.assertIn('data', response_data)
        self.assertEqual(len(response_data['data']), 1)

    def test_invalid_access_to_views(self):
        """
        Тест недоступности аналитических представлений для неавторизованного пользователя.

        Проверяет, что неавторизованные пользователи или обычные пользователи (без прав администратора)
        не имеют доступа к панели аналитики, обновлению данных и API получения аналитики.
        """
        # Проверка доступа к панели аналитики без авторизации (редирект на страницу входа)
        response = self.client.get(reverse('analytics:analytics_dashboard'))
        self.assertEqual(response.status_code, 302)  # Неавторизованный пользователь должен быть перенаправлен на страницу входа

        # Проверка доступа к обновлению аналитики без авторизации
        response = self.client.get(reverse('analytics:update_analytics'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа

        # Попытка отправить запрос к API с недопустимым пользователем (не администратор)
        self.regular_profile.refresh_from_db()
        self.assertEqual(self.regular_profile.telegram_id, '654321')

        data = {
            'period_start': str(self.order_1.delivery_date),
            'period_end': str(self.order_1.delivery_date),
            'product_id': self.product_1.id,
            'telegram_id': self.regular_profile.telegram_id  # Telegram ID обычного пользователя
        }
        response = self.client.post(reverse('analytics:get_analytics_data'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)  # Ожидается статус 403 (доступ запрещен)

    def test_invalid_telegram_id_access(self):
        """
        Тест недоступности API для некорректного telegram_id.

        Проверяет, что API не предоставляет доступ к данным аналитики, если передан некорректный `telegram_id`.
        """
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
        response = self.client.post(reverse('analytics:get_analytics_data'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        response_data = response.json()
        self.assertEqual(response_data['status'], 'error')
        self.assertEqual(response_data['message'], 'Пользователь не найден.')
