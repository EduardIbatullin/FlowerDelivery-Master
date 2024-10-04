# apps/analytics/tests/test_forms.py

from datetime import date  # Импортируем модуль для работы с датами

from django.test import TestCase  # Импортируем TestCase для создания тестов

from apps.analytics.forms import AnalyticsFilterForm  # Импортируем форму фильтрации аналитики AnalyticsFilterForm
from apps.catalog.models import Product  # Импортируем модель продукта Product


class AnalyticsFilterFormTest(TestCase):
    """
    Набор тестов для формы фильтрации аналитики `AnalyticsFilterForm`.

    Включает тесты для проверки корректной инициализации формы, а также правильной обработки различных
    входных данных (периоды времени, пользовательские даты и т.д.).
    """

    @classmethod
    def setUpTestData(cls):
        """
        Метод для инициализации тестовых данных перед запуском тестов.

        Создает несколько объектов `Product` (букетов), которые используются для тестирования валидации
        формы и логики работы фильтрации.
        """
        cls.product1 = Product.objects.create(name="Букет №1", price=1500.0, description="Красивый букет")
        cls.product2 = Product.objects.create(name="Букет №2", price=2500.0, description="Элегантный букет")

    def test_form_initialization(self):
        """
        Тестирование инициализации формы.

        Проверяет, что все необходимые поля присутствуют в форме после ее инициализации.
        """
        form = AnalyticsFilterForm()
        self.assertIn('period', form.fields)
        self.assertIn('product', form.fields)
        self.assertIn('custom_start_date', form.fields)
        self.assertIn('custom_end_date', form.fields)

    def test_form_valid_data(self):
        """
        Тестирование формы с корректными данными.

        Проверяет, что форма считается валидной при передаче корректных данных, включая выбор периода
        и конкретного продукта.
        """
        form_data = {
            'period': '3_months',
            'product': self.product1.id,
            'custom_start_date': '',
            'custom_end_date': ''
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_period(self):
        """
        Тестирование формы с некорректным периодом.

        Проверяет, что форма считается недействительной при передаче некорректного значения периода.
        Ожидается, что валидация формы завершится ошибкой и поле 'period' будет содержать сообщение об ошибке.
        """
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
        """
        Тестирование пользовательских дат без выбора 'custom' периода.

        Проверяет, что передача произвольных дат (custom_start_date и custom_end_date) не влияет на
        валидацию формы, если выбран стандартный период времени (например, 'year').
        """
        form_data = {
            'period': 'year',
            'product': '',
            'custom_start_date': '2024-01-01',
            'custom_end_date': '2024-12-31'
        }
        form = AnalyticsFilterForm(data=form_data)
        self.assertTrue(form.is_valid())  # Пользовательские даты не должны влиять при периоде, отличном от 'custom'

    def test_form_valid_custom_period(self):
        """
        Тестирование формы с корректным кастомным периодом.

        Проверяет, что форма считается валидной при передаче корректных пользовательских дат (custom_start_date и custom_end_date)
        и выборе периода 'custom'.
        """
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

        Проверяет, что форма считается недействительной при передаче некорректных дат (например, если конец периода
        указан раньше начала периода).
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
