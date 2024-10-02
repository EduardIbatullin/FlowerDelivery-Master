# apps/users/tests/test_models.py

from django.test import TestCase
from apps.users.models import CustomUser, Profile
from datetime import date

class CustomUserModelTest(TestCase):
    def setUp(self):
        """Создание тестового пользователя."""
        self.user = CustomUser.objects.create(
            username='testuser',
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            birth_date=date(1990, 1, 1)  # Используем объект date вместо строки
        )

    def test_create_user(self):
        """Проверка создания пользователя с заданными данными."""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Иван')
        self.assertEqual(self.user.last_name, 'Иванов')
        self.assertEqual(self.user.patronymic, 'Иванович')
        self.assertEqual(self.user.birth_date, date(1990, 1, 1))  # Исправляем формат даты

    def test_user_str_representation(self):
        """Проверка строкового представления пользователя."""
        self.assertEqual(str(self.user), 'testuser')


class ProfileModelTest(TestCase):
    def setUp(self):
        """Создание тестового пользователя и профиля."""
        self.user = CustomUser.objects.create(username='testuser', first_name='Иван', last_name='Иванов')
        # Используем уже существующий профиль вместо создания нового
        self.profile = self.user.profile
        self.profile.delivery_address = 'Тестовый адрес'
        self.profile.phone = '1234567890'
        self.profile.email = 'testuser@example.com'
        self.profile.telegram_id = '123456789'
        self.profile.save()

    def test_create_profile(self):
        """Проверка создания профиля для пользователя."""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.delivery_address, 'Тестовый адрес')
        self.assertEqual(self.profile.phone, '1234567890')
        self.assertEqual(self.profile.email, 'testuser@example.com')
        self.assertEqual(self.profile.telegram_id, '123456789')

    def test_profile_str_representation(self):
        """Проверка строкового представления профиля."""
        self.assertEqual(str(self.profile), f'Profile of {self.user.username}')

    def test_profile_user_relation(self):
        """Проверка отношения профиля к пользователю."""
        self.assertEqual(self.user.profile, self.profile)
