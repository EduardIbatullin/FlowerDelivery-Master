# apps/analytics/tests/test_models.py

from django.test import TestCase
from django.utils import timezone
from apps.catalog.models import Product
from apps.analytics.models import SalesAnalytics


class SalesAnalyticsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестовый продукт
        cls.product = Product.objects.create(
            name="Тестовый букет",
            price=2500.0,
            description="Тестовое описание букета",
            is_available=True
        )

        # Создаем объект SalesAnalytics для тестирования
        cls.sales_analytics = SalesAnalytics.objects.create(
            product=cls.product,
            total_sales=10,
            total_revenue=25000.0,
            average_order_value=2500.0,
            period_start=timezone.now().date() - timezone.timedelta(days=30),
            period_end=timezone.now().date()
        )

    def test_sales_analytics_creation(self):
        """Тест создания объекта SalesAnalytics."""
        analytics = SalesAnalytics.objects.get(id=self.sales_analytics.id)
        self.assertEqual(analytics.product.name, "Тестовый букет")
        self.assertEqual(analytics.total_sales, 10)
        self.assertEqual(float(analytics.total_revenue), 25000.0)
        self.assertEqual(float(analytics.average_order_value), 2500.0)
        self.assertEqual(analytics.period_start, timezone.now().date() - timezone.timedelta(days=30))
        self.assertEqual(analytics.period_end, timezone.now().date())

    def test_sales_analytics_str(self):
        """Тест строкового представления объекта SalesAnalytics."""
        self.assertEqual(
            str(self.sales_analytics),
            f"Аналитика продаж: {self.product.name} ({self.sales_analytics.period_start} - {self.sales_analytics.period_end})"
        )

    def test_sales_analytics_related_product(self):
        """Тест связи с продуктом и удаление объекта SalesAnalytics при удалении продукта."""
        # Удаление продукта должно привести к удалению соответствующей аналитики продаж
        self.product.delete()
        with self.assertRaises(SalesAnalytics.DoesNotExist):
            SalesAnalytics.objects.get(id=self.sales_analytics.id)

    def test_sales_analytics_field_defaults(self):
        """Тест значений по умолчанию полей модели SalesAnalytics."""
        new_analytics = SalesAnalytics.objects.create(
            product=self.product,
            period_start=timezone.now().date(),
            period_end=timezone.now().date()
        )
        self.assertEqual(new_analytics.total_sales, 0)
        self.assertEqual(float(new_analytics.total_revenue), 0.00)
        self.assertEqual(float(new_analytics.average_order_value), 0.00)
