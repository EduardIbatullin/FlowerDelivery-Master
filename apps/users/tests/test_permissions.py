# apps/users/tests/test_permissions.py

from django.test import TestCase  # Импорт базового класса для создания тестов Django
from django.contrib.auth import get_user_model  # Импорт функции для получения пользовательской модели
from django.contrib.auth.models import Group  # Импорт модели группы пользователей

from apps.users.permissions import is_employee, is_admin  # Импорт тестируемых функций для проверки прав доступа

# Получение пользовательской модели для создания тестовых пользователей
User = get_user_model()


class PermissionsTest(TestCase):
    """
    Набор тестов для проверки пользовательских прав и ролей.

    Тестируемые сценарии:
    1. Проверка функции `is_employee`.
    2. Проверка функции `is_admin`.
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

    def test_is_employee(self):
        """
        Проверка функции `is_employee` на разных пользователях.

        Убеждается, что функция корректно определяет принадлежность пользователя к группе 'Сотрудники'.

        Ожидаемый результат:
            - Обычный пользователь не является сотрудником.
            - Пользователь в группе 'Сотрудники' определяется как сотрудник.
            - Пользователь в группе 'Администраторы' не является сотрудником.
            - Суперпользователь не определяется как сотрудник.
        """
        self.assertFalse(is_employee(self.user))          # Обычный пользователь не является сотрудником
        self.assertTrue(is_employee(self.employee))       # Пользователь в группе 'Сотрудники' определяется как сотрудник
        self.assertFalse(is_employee(self.admin))         # Администратор не является сотрудником
        self.assertFalse(is_employee(self.superuser))     # Суперпользователь не является сотрудником

    def test_is_admin(self):
        """
        Проверка функции `is_admin` на разных пользователях.

        Убеждается, что функция корректно определяет принадлежность пользователя к группе 'Администраторы' или наличие
        статуса суперпользователя.

        Ожидаемый результат:
            - Обычный пользователь не является администратором.
            - Пользователь в группе 'Сотрудники' не является администратором.
            - Пользователь в группе 'Администраторы' определяется как администратор.
            - Суперпользователь определяется как администратор.
        """
        self.assertFalse(is_admin(self.user))             # Обычный пользователь не является администратором
        self.assertFalse(is_admin(self.employee))         # Сотрудник не является администратором
        self.assertTrue(is_admin(self.admin))             # Пользователь в группе 'Администраторы' определяется как администратор
        self.assertTrue(is_admin(self.superuser))         # Суперпользователь определяется как администратор
