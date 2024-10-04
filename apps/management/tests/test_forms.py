# apps/management/tests/test_forms.py

from django.test import TestCase  # Импорт TestCase для создания тестов

from apps.management.forms import OrderFilterForm, OrderStatusForm  # Импорт форм для тестирования
from apps.orders.models import Order  # Импорт модели Order для работы с тестовыми данными
from apps.users.models import CustomUser  # Импорт кастомной модели пользователя для создания тестовых данных


class OrderStatusFormTest(TestCase):
    """
    Набор тестов для формы изменения статуса заказа `OrderStatusForm`.

    Включает тесты для проверки корректной работы формы, правильной обработки атрибутов полей,
    а также тесты на проверку корректности логики изменения статуса заказа.
    """

    def setUp(self):
        """
        Метод для инициализации тестовых данных перед каждым тестом.

        Создает тестового пользователя и тестовый заказ, которые будут использоваться в тестах.
        """
        # Создаем тестового пользователя
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')

        # Создаем тестовый заказ, указывая необходимые поля
        self.order = Order.objects.create(
            user=self.user,
            delivery_address='Тестовый адрес',  # Адрес доставки для заказа
            contact_phone='1234567890',  # Контактный телефон для заказа
            status='В обработке',  # Статус заказа
            complete=False  # Заказ не завершен
        )

    def test_order_status_form_fields(self):
        """
        Проверка наличия и корректности полей в форме OrderStatusForm.

        Убеждаемся, что поле 'status' присутствует в форме и его метка отображается правильно.
        """
        form = OrderStatusForm(instance=self.order)
        self.assertIn('status', form.fields)  # Проверка наличия поля 'status' в форме
        self.assertEqual(form.fields['status'].label, 'Выберите новый статус')  # Проверка метки поля

    def test_order_status_form_disabled_for_completed_order(self):
        """
        Проверка, что поле 'status' не активно (заблокировано для изменения), если заказ завершен.

        Форма должна блокировать изменение статуса, если поле 'complete' в модели Order установлено в True.
        """
        # Устанавливаем заказ как завершенный
        self.order.complete = True
        form = OrderStatusForm(instance=self.order)

        # Проверка, что поле 'status' заблокировано для редактирования
        self.assertTrue(form.fields['status'].widget.attrs.get('disabled'))


class OrderFilterFormTest(TestCase):
    """
    Набор тестов для формы фильтрации заказов `OrderFilterForm`.

    Включает тесты для проверки корректной инициализации полей формы, а также правильности
    отображения вариантов выбора (choices) для фильтров по статусу и завершенности заказа.
    """

    def test_order_filter_form_fields(self):
        """
        Проверка наличия и корректности полей в форме OrderFilterForm.

        Убеждаемся, что поля 'status' и 'complete' присутствуют в форме и корректно инициализируются.
        """
        form = OrderFilterForm()
        # Проверка наличия поля 'status' для фильтрации по статусу заказа
        self.assertIn('status', form.fields)
        # Проверка наличия поля 'complete' для фильтрации по завершенности заказа
        self.assertIn('complete', form.fields)

    def test_order_filter_form_choices(self):
        """
        Проверка корректности вариантов выбора (choices) для полей формы.

        Убеждаемся, что варианты выбора для полей 'status' и 'complete' совпадают с ожидаемыми значениями.
        """
        form = OrderFilterForm()
        status_choices = form.fields['status'].choices
        complete_choices = form.fields['complete'].choices

        # Проверка наличия опции 'Все' и других значений в поле 'status'
        self.assertEqual(status_choices[0], ('', 'Все'))  # Проверка первой опции - 'Все'
        self.assertIn(('В обработке', 'В обработке'), status_choices)  # Проверка наличия статуса 'В обработке'

        # Проверка корректности вариантов выбора для поля 'complete'
        self.assertEqual(complete_choices, [('', 'Все'), ('True', 'Завершен'), ('False', 'Не завершен')])  # Опции для завершенности заказа
