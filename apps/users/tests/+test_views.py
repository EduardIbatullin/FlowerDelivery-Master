# apps/users/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from apps.users.models import Profile
import json

User = get_user_model()


class UsersViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создание тестового пользователя
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            birth_date='1990-01-01'
        )

        # Удаление профиля, если он уже существует
        if hasattr(cls.user, 'profile'):
            cls.user.profile.delete()

        # Создание нового профиля для тестов
        cls.profile = Profile.objects.create(
            user=cls.user,
            email='testuser@example.com',
            telegram_id='123456789'
        )

    def test_login_view(self):
        """Проверка страницы входа."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_register_view(self):
        """Проверка страницы регистрации."""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_profile_view(self):
        """Проверка страницы профиля."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view(self):
        """Проверка страницы редактирования профиля."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_delete_account_view(self):
        """Проверка удаления аккаунта."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('users:delete_account'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_save_telegram_id_view(self):
        """Проверка сохранения telegram_id."""
        data = {
            'user_id': self.user.id,
            'telegram_id': '987654321'
        }
        response = self.client.post(reverse('users:save_telegram_id'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.telegram_id, '987654321')

    def test_get_user_data_view(self):
        """Проверка получения данных пользователя."""
        data = {'user_id': self.user.id}
        response = self.client.post(reverse('users:get_user_data'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.user.username)

    def test_get_user_data_by_telegram_id_view(self):
        """Проверка получения данных пользователя по telegram_id."""
        data = {'telegram_id': self.profile.telegram_id}
        response = self.client.post(reverse('users:get_user_data_by_telegram_id'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_data']['first_name'], self.user.first_name)

    def test_logout_view(self):
        """Проверка выхода из системы."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)
