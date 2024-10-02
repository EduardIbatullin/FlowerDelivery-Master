# apps/orders/tests/test_forms.py

from django.test import TestCase
from apps.orders.forms import OrderForm
from datetime import date, time


class OrderFormTest(TestCase):
    def setUp(self):
        # Инициализация тестовых данных
        self.valid_data = {
            'delivery_address': 'Тестовый адрес',
            'contact_phone': '1234567890',
            'delivery_date': date.today(),
            'delivery_time': time(14, 30),  # 14:30
            'additional_info': 'Тестовая информация',
            'email_notifications': True,
            'telegram_notifications': False,
            'total_price': 1500.00
        }

    def test_order_form_valid_data(self):
        """Тест формы заказа с валидными данными."""
        form = OrderForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_order_form_missing_required_fields(self):
        """Тест формы заказа с отсутствующими обязательными полями."""
        # Удаляем обязательные поля для проверки валидации
        invalid_data = self.valid_data.copy()
        invalid_data.pop('contact_phone')
        invalid_data.pop('delivery_address')

        form = OrderForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('contact_phone', form.errors)
        self.assertIn('delivery_address', form.errors)

    def test_order_form_field_labels(self):
        """Тест отображения меток полей формы."""
        form = OrderForm()
        self.assertEqual(form.fields['delivery_address'].label, 'Адрес доставки')
        self.assertEqual(form.fields['contact_phone'].label, 'Контактный телефон')
        self.assertEqual(form.fields['delivery_date'].label, 'Дата доставки')
        self.assertEqual(form.fields['delivery_time'].label, 'Время доставки')
        self.assertEqual(form.fields['additional_info'].label, 'Дополнительная информация')
        self.assertEqual(form.fields['email_notifications'].label, 'Получать уведомления по e-mail')  # Изменено на корректное значение
        self.assertEqual(form.fields['telegram_notifications'].label, 'Получать уведомления по Telegram')  # Изменено на корректное значение

    def test_order_form_initial_data(self):
        """Тест начальных данных формы."""
        form = OrderForm(initial=self.valid_data)
        self.assertEqual(form.initial['delivery_address'], 'Тестовый адрес')
        self.assertEqual(form.initial['contact_phone'], '1234567890')
        self.assertEqual(form.initial['delivery_date'], date.today())
        self.assertEqual(form.initial['delivery_time'], time(14, 30))
        self.assertEqual(form.initial['additional_info'], 'Тестовая информация')
        self.assertTrue(form.initial['email_notifications'])
        self.assertFalse(form.initial['telegram_notifications'])
        self.assertEqual(form.initial['total_price'], 1500.00)
