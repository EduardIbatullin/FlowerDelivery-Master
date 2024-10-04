# apps/orders/tests/test_forms.py

from datetime import date, time  # Импортируем для работы с датами и временем

from django.test import TestCase  # Импортируем TestCase для создания тестов форм

from apps.orders.forms import OrderForm  # Импортируем форму заказа для тестирования


class OrderFormTest(TestCase):
    """
    Набор тестов для формы заказа `OrderForm`.

    Проверяет валидность формы, наличие обязательных полей, метки полей формы
    и начальные данные для создания заказа.
    """

    def setUp(self):
        """
        Метод для инициализации тестовых данных перед каждым тестом.

        Создает словарь с валидными данными, которые будут использоваться в тестах.
        """
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
        """
        Тест формы заказа с валидными данными.

        Проверяет, что форма действительна при наличии всех необходимых полей.
        """
        form = OrderForm(data=self.valid_data)
        self.assertTrue(form.is_valid())  # Проверяем, что форма валидна

    def test_order_form_missing_required_fields(self):
        """
        Тест формы заказа с отсутствующими обязательными полями.

        Проверяет, что форма становится недействительной при отсутствии обязательных полей,
        и что ошибки указывают на эти поля.
        """
        # Удаляем обязательные поля для проверки валидации
        invalid_data = self.valid_data.copy()
        invalid_data.pop('contact_phone')
        invalid_data.pop('delivery_address')

        form = OrderForm(data=invalid_data)
        self.assertFalse(form.is_valid())  # Проверяем, что форма невалидна
        self.assertIn('contact_phone', form.errors)  # Проверяем наличие ошибки по полю 'contact_phone'
        self.assertIn('delivery_address', form.errors)  # Проверяем наличие ошибки по полю 'delivery_address'

    def test_order_form_field_labels(self):
        """
        Тест отображения меток полей формы.

        Проверяет, что метки полей формы отображаются корректно.
        """
        form = OrderForm()
        self.assertEqual(form.fields['delivery_address'].label, 'Адрес доставки')  # Проверка метки
        self.assertEqual(form.fields['contact_phone'].label, 'Контактный телефон')  # Проверка метки
        self.assertEqual(form.fields['delivery_date'].label, 'Дата доставки')  # Проверка метки
        self.assertEqual(form.fields['delivery_time'].label, 'Время доставки')  # Проверка метки
        self.assertEqual(form.fields['additional_info'].label, 'Дополнительная информация')  # Проверка метки
        self.assertEqual(form.fields['email_notifications'].label, 'Получать уведомления по e-mail')  # Проверка метки
        self.assertEqual(form.fields['telegram_notifications'].label, 'Получать уведомления по Telegram')  # Проверка метки

    def test_order_form_initial_data(self):
        """
        Тест начальных данных формы.

        Проверяет, что начальные данные формы устанавливаются корректно.
        """
        form = OrderForm(initial=self.valid_data)
        self.assertEqual(form.initial['delivery_address'], 'Тестовый адрес')  # Проверка начального значения
        self.assertEqual(form.initial['contact_phone'], '1234567890')  # Проверка начального значения
        self.assertEqual(form.initial['delivery_date'], date.today())  # Проверка начального значения
        self.assertEqual(form.initial['delivery_time'], time(14, 30))  # Проверка начального значения
        self.assertEqual(form.initial['additional_info'], 'Тестовая информация')  # Проверка начального значения
        self.assertTrue(form.initial['email_notifications'])  # Проверка начального значения
        self.assertFalse(form.initial['telegram_notifications'])  # Проверка начального значения
        self.assertEqual(form.initial['total_price'], 1500.00)  # Проверка начального значения
