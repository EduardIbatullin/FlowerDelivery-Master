# apps/management/tests/test_forms.py

from django.test import TestCase
from apps.management.forms import OrderStatusForm, OrderFilterForm
from apps.orders.models import Order
from apps.users.models import CustomUser  # Импортируем кастомного пользователя


class OrderStatusFormTest(TestCase):
    def setUp(self):
        # Создание тестового пользователя, так как Order имеет связь с пользователем
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

        # Создаем тестовый заказ с учетом существующих полей
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Тестовый адрес',  # Поле адреса доставки
            contact_phone='1234567890',  # Поле контактного телефона
            status='В обработке',
            complete=False
        )

    def test_order_status_form_fields(self):
        """Проверка наличия и корректности полей в форме OrderStatusForm."""
        form = OrderStatusForm(instance=self.order)
        self.assertIn('status', form.fields)
        self.assertEqual(form.fields['status'].label, 'Выберите новый статус')

    def test_order_status_form_disabled_for_completed_order(self):
        """Проверка, что поле 'status' не активно, если заказ завершен."""
        # Устанавливаем заказ как завершенный
        self.order.complete = True
        form = OrderStatusForm(instance=self.order)
        self.assertTrue(form.fields['status'].widget.attrs.get('disabled'))


class OrderFilterFormTest(TestCase):
    def test_order_filter_form_fields(self):
        """Проверка наличия и корректности полей в форме OrderFilterForm."""
        form = OrderFilterForm()
        self.assertIn('status', form.fields)
        self.assertIn('complete', form.fields)

    def test_order_filter_form_choices(self):
        """Проверка корректности вариантов выбора для полей формы."""
        form = OrderFilterForm()
        status_choices = form.fields['status'].choices
        complete_choices = form.fields['complete'].choices

        # Проверка наличия нужных значений
        self.assertEqual(status_choices[0], ('', 'Все'))
        self.assertIn(('В обработке', 'В обработке'), status_choices)
        self.assertEqual(complete_choices, [('', 'Все'), ('True', 'Завершен'), ('False', 'Не завершен')])
