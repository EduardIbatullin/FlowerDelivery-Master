# apps/users/tests/test_permissions.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from apps.users.permissions import is_employee, is_admin

User = get_user_model()


class PermissionsTest(TestCase):
    def setUp(self):
        """Создание тестовых пользователей и групп."""
        # Создаем группы
        self.employees_group = Group.objects.create(name='Сотрудники')
        self.admin_group = Group.objects.create(name='Администраторы')

        # Создаем тестового пользователя
        self.user = User.objects.create(username='testuser', first_name='Иван', last_name='Иванов')

        # Создаем тестового сотрудника
        self.employee = User.objects.create(username='employeeuser', first_name='Петр', last_name='Петров')
        self.employee.groups.add(self.employees_group)

        # Создаем тестового администратора
        self.admin = User.objects.create(username='adminuser', first_name='Сергей', last_name='Сергеев')
        self.admin.groups.add(self.admin_group)

        # Создаем суперпользователя
        self.superuser = User.objects.create_superuser(username='superuser', password='superpassword')

    def test_is_employee(self):
        """Проверка функции is_employee."""
        self.assertFalse(is_employee(self.user))          # Обычный пользователь не является сотрудником
        self.assertTrue(is_employee(self.employee))       # Пользователь в группе 'Сотрудники' является сотрудником
        self.assertFalse(is_employee(self.admin))         # Администратор не является сотрудником
        self.assertFalse(is_employee(self.superuser))     # Суперпользователь не является сотрудником

    def test_is_admin(self):
        """Проверка функции is_admin."""
        self.assertFalse(is_admin(self.user))             # Обычный пользователь не является администратором
        self.assertFalse(is_admin(self.employee))         # Сотрудник не является администратором
        self.assertTrue(is_admin(self.admin))             # Пользователь в группе 'Администраторы' является администратором
        self.assertTrue(is_admin(self.superuser))         # Суперпользователь является администратором
