# apps/analytics/tests/test_forms.py

from django.test import TestCase
from apps.analytics.forms import AnalyticsFilterForm
from apps.catalog.models import Product
from datetime import date


class AnalyticsFilterFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестовых данных для продуктов (букетов)
        cls.product1 = Product.objects.create(name="Букет №1", price=1500.0, description="Красивый букет")
        cls.product2 = Product.objects.create(name="Букет №2", price=2500.0, description="Элегантный букет")

    def test_form_initialization(self):
        """Тестирование инициализации формы."""
        form = AnalyticsFilterForm()
        self.assertIn('period', form.fields)
        self.assertIn('product', form.fields)
        self.assertIn('custom_start_date', form.fields)
        self.assertIn('custom_end_date', form.fields)

    def test_form_valid_data(self):
        """Тестирование формы с корректными данными."""
        form_data = {
            'period': '3_months',
            'product': self.product1.id,
            'custom_start_date': '',
            'custom_end_date': ''
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_period(self):
        """Тестирование формы с некорректным периодом."""
        form_data = {
            'period': 'invalid_period',
            'product': self.product1.id,
            'custom_start_date': '',
            'custom_end_date': ''
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('period', form.errors)

    def test_form_custom_date_without_period(self):
        """Тестирование пользовательских дат без выбора 'custom' периода."""
        form_data = {
            'period': 'year',
            'product': '',
            'custom_start_date': '2024-01-01',
            'custom_end_date': '2024-12-31'
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())  # Custom dates should not affect when period is not 'custom'

    def test_form_valid_custom_period(self):
        """Тестирование формы с корректным кастомным периодом."""
        form_data = {
            'period': 'custom',
            'product': '',
            'custom_start_date': '2024-01-01',
            'custom_end_date': '2024-12-31'
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_custom_period(self):
        """
        Тестирование формы с некорректными пользовательскими датами (конец раньше начала).
        """
        form_data = {
            'period': 'custom',
            'custom_start_date': '2024-12-31',  # Начало периода позже конца периода
            'custom_end_date': '2024-01-01'
        }
        form = AnalyticsFilterForm(data=form_data)

        # Ожидаем, что форма будет недействительной из-за неправильных дат
        self.assertFalse(form.is_valid(), f"Форма должна быть недействительна, но она действительна: {form.errors}")

        # Проверяем, что ошибка валидации связана с датами
        self.assertIn('Конец периода не может быть раньше начала.', form.errors.get('__all__', []))
