# apps/users/tests/test_templatetags.py

from django.test import TestCase  # Импорт базового класса для создания тестов Django
from django.contrib.auth import get_user_model  # Импорт функции для получения пользовательской модели
from django.contrib.auth.models import Group  # Импорт модели группы пользователей

from apps.users.templatetags.custom_filters import check_is_admin, check_is_employee  # Импорт тестируемых фильтров

# Получение пользовательской модели для создания тестовых пользователей
User = get_user_model()


class CustomFiltersTest(TestCase):
    """
    Набор тестов для проверки пользовательских фильтров шаблонов.

    Тестируемые сценарии:
    1. Проверка фильтра `check_is_admin`.
    2. Проверка фильтра `check_is_employee`.
    """

    def setUp(self):
        """
        Создание тестовых данных: пользователей и групп.

        Устанавливает начальные данные для всех тестов в классе:
        1. Группы пользователей: 'Сотрудники' и 'Администраторы'.
        2. Тестовые пользователи: обычный пользователь, сотрудник, администратор и суперпользователь.
        """
        # Создаем группы пользователей
        self.employees_group = Group.objects.create(name='Сотрудники')
        self.admin_group = Group.objects.create(name='Администраторы')

        # Создаем тестового обычного пользователя
        self.user = User.objects.create(username='testuser', first_name='Иван', last_name='Иванов')

        # Создаем тестового сотрудника и добавляем его в группу 'Сотрудники'
        self.employee = User.objects.create(username='employeeuser', first_name='Петр', last_name='Петров')
        self.employee.groups.add(self.employees_group)

        # Создаем тестового администратора и добавляем его в группу 'Администраторы'
        self.admin = User.objects.create(username='adminuser', first_name='Сергей', last_name='Сергеев')
        self.admin.groups.add(self.admin_group)

        # Создаем суперпользователя с правами администратора
        self.superuser = User.objects.create_superuser(username='superuser', password='superpassword')

    def test_check_is_admin(self):
        """
        Проверка фильтра `check_is_admin` на разных пользователях.

        Убеждается, что фильтр корректно определяет принадлежность пользователя к группе 'Администраторы' или наличие статуса суперпользователя.

        Ожидаемый результат:
            - Обычный пользователь не является администратором.
            - Пользователь в группе 'Сотрудники' не является администратором.
            - Пользователь в группе 'Администраторы' определяется как администратор.
            - Суперпользователь определяется как администратор.
        """
        self.assertFalse(check_is_admin(self.user))             # Обычный пользователь не является администратором
        self.assertFalse(check_is_admin(self.employee))         # Сотрудник не является администратором
        self.assertTrue(check_is_admin(self.admin))             # Пользователь в группе 'Администраторы' является администратором
        self.assertTrue(check_is_admin(self.superuser))         # Суперпользователь определяется как администратор

    def test_check_is_employee(self):
        """
        Проверка фильтра `check_is_employee` на разных пользователях.

        Убеждается, что фильтр корректно определяет принадлежность пользователя к группе 'Сотрудники'.

        Ожидаемый результат:
            - Обычный пользователь не является сотрудником.
            - Пользователь в группе 'Сотрудники' определяется как сотрудник.
            - Пользователь в группе 'Администраторы' не является сотрудником.
            - Суперпользователь не определяется как сотрудник.
        """
        self.assertFalse(check_is_employee(self.user))          # Обычный пользователь не является сотрудником
        self.assertTrue(check_is_employee(self.employee))       # Пользователь в группе 'Сотрудники' определяется как сотрудник
        self.assertFalse(check_is_employee(self.admin))         # Администратор не является сотрудником
        self.assertFalse(check_is_employee(self.superuser))     # Суперпользователь не является сотрудником
