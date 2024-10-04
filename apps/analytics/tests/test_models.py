# apps/analytics/tests/test_models.py

from django.test import TestCase  # Импортируем TestCase для создания тестов моделей
from django.utils import timezone  # Импортируем timezone для работы с временными значениями

from apps.analytics.models import SalesAnalytics  # Импорт модели SalesAnalytics для тестирования аналитических данных
from apps.catalog.models import Product  # Импорт модели Product для тестирования связи с аналитическими данными


class SalesAnalyticsModelTest(TestCase):
    """
    Набор тестов для модели `SalesAnalytics`.

    Проверяет корректное создание объектов модели, связь с продуктами, значения по умолчанию,
    а также строковое представление модели.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Инициализация тестовых данных перед запуском тестов.

        Создает тестовый объект `Product` и связанный с ним объект `SalesAnalytics` для проверки работы модели.
        Данные инициализируются только один раз для всего набора тестов.
        """
        # Создание тестового продукта (букета)
        cls.product = Product.objects.create(
            name="Тестовый букет",
            price=2500.0,
            description="Тестовое описание букета",
            is_available=True
        )

        # Создание объекта SalesAnalytics для тестирования
        cls.sales_analytics = SalesAnalytics.objects.create(
            product=cls.product,
            total_sales=10,
            total_revenue=25000.0,
            average_order_value=2500.0,
            period_start=timezone.now().date() - timezone.timedelta(days=30),
            period_end=timezone.now().date()
        )

    def test_sales_analytics_creation(self):
        """
        Тест создания объекта SalesAnalytics.

        Проверяет, что объект аналитики продаж создается с корректными данными и сохраняется в базе данных.
        """
        analytics = SalesAnalytics.objects.get(id=self.sales_analytics.id)
        self.assertEqual(analytics.product.name, "Тестовый букет")
        self.assertEqual(analytics.total_sales, 10)
        self.assertEqual(float(analytics.total_revenue), 25000.0)
        self.assertEqual(float(analytics.average_order_value), 2500.0)
        self.assertEqual(analytics.period_start, timezone.now().date() - timezone.timedelta(days=30))
        self.assertEqual(analytics.period_end, timezone.now().date())

    def test_sales_analytics_str(self):
        """
        Тест строкового представления объекта SalesAnalytics.

        Проверяет, что строковое представление объекта соответствует ожидаемому формату:
        "Аналитика продаж: <Название продукта> (<Дата начала периода> - <Дата конца периода>)".
        """
        expected_str = f"Аналитика продаж: {self.product.name} ({self.sales_analytics.period_start} - {self.sales_analytics.period_end})"
        self.assertEqual(str(self.sales_analytics), expected_str)

    def test_sales_analytics_related_product(self):
        """
        Тест связи с продуктом и удаление объекта SalesAnalytics при удалении продукта.

        Проверяет, что при удалении связанного объекта `Product` соответствующий объект `SalesAnalytics` также удаляется из базы данных.
        """
        # Удаление продукта должно привести к удалению соответствующей аналитики продаж
        self.product.delete()
        with self.assertRaises(SalesAnalytics.DoesNotExist):
            SalesAnalytics.objects.get(id=self.sales_analytics.id)

    def test_sales_analytics_field_defaults(self):
        """
        Тест значений по умолчанию полей модели SalesAnalytics.

        Проверяет, что поля `total_sales`, `total_revenue` и `average_order_value` модели имеют
        корректные значения по умолчанию (нулевые) при создании объекта без указания этих значений.
        """
        new_analytics = SalesAnalytics.objects.create(
            product=self.product,
            period_start=timezone.now().date(),
            period_end=timezone.now().date()
        )
        self.assertEqual(new_analytics.total_sales, 0)
        self.assertEqual(float(new_analytics.total_revenue), 0.00)
        self.assertEqual(float(new_analytics.average_order_value), 0.00)
