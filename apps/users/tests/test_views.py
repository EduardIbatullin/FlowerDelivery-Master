# apps/users/tests/test_views.py

import json  # Импорт модуля для работы с JSON-данными

from django.test import TestCase  # Импорт базового класса для создания тестов Django
from django.urls import reverse  # Импорт функции для создания URL-обратных маршрутов
from django.contrib.auth import get_user_model  # Импорт функции для получения пользовательской модели
from django.contrib.auth import authenticate, login, logout  # Импорт функций аутентификации и управления сеансами

from apps.users.models import Profile  # Импорт модели профиля пользователя

# Получение пользовательской модели для создания тестовых пользователей
User = get_user_model()


class UsersViewsTest(TestCase):
    """
    Набор тестов для проверки представлений приложения `users`.

    Тестируемые сценарии:
    1. Проверка отображения и корректного рендеринга страниц: вход, регистрация, профиль, редактирование профиля.
    2. Проверка удаления аккаунта пользователя.
    3. Проверка сохранения Telegram ID.
    4. Проверка получения данных пользователя.
    5. Проверка выхода пользователя из системы.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Создание тестового пользователя и профиля для проверки представлений.

        Устанавливает начальные данные для всех тестов в классе.

        Входные данные:
            - username: 'testuser'.
            - password: 'testpassword'.
            - first_name: 'Иван'.
            - last_name: 'Иванов'.
            - patronymic: 'Иванович'.
            - birth_date: '1990-01-01'.
            - email: 'testuser@example.com'.
            - telegram_id: '123456789'.
        """
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            birth_date='1990-01-01'
        )

        # Удаляем существующий профиль, если он есть
        if hasattr(cls.user, 'profile'):
            cls.user.profile.delete()

        # Создаем профиль для тестового пользователя
        cls.profile = Profile.objects.create(
            user=cls.user,
            email='testuser@example.com',
            telegram_id='123456789'
        )

    def test_login_view(self):
        """
        Проверка отображения страницы входа.

        Убеждается, что страница входа рендерится корректно и использует правильный шаблон.

        Ожидаемый результат:
            - HTTP статус 200.
            - Использование шаблона 'auth/login.html'.
        """
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    def test_register_view(self):
        """
        Проверка отображения страницы регистрации.

        Убеждается, что страница регистрации рендерится корректно и использует правильный шаблон.

        Ожидаемый результат:
            - HTTP статус 200.
            - Использование шаблона 'auth/register.html'.
        """
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/register.html')

    def test_profile_view(self):
        """
        Проверка отображения страницы профиля пользователя.

        Убеждается, что страница профиля рендерится корректно и использует правильный шаблон.

        Ожидаемый результат:
            - HTTP статус 200.
            - Использование шаблона 'users/profile.html'.
        """
        self.client.login(username='testuser', password='testpassword')  # Авторизация пользователя
        response = self.client.get(reverse('users:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_edit_profile_view(self):
        """
        Проверка отображения страницы редактирования профиля.

        Убеждается, что страница редактирования профиля рендерится корректно и использует правильный шаблон.

        Ожидаемый результат:
            - HTTP статус 200.
            - Использование шаблона 'users/edit_profile.html'.
        """
        self.client.login(username='testuser', password='testpassword')  # Авторизация пользователя
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')

    def test_delete_account_view(self):
        """
        Проверка удаления аккаунта пользователя.

        Убеждается, что аккаунт пользователя удаляется корректно и происходит редирект на главную страницу.

        Ожидаемый результат:
            - Успешный редирект на главную страницу.
            - Пользователь удален из базы данных.
        """
        self.client.login(username='testuser', password='testpassword')  # Авторизация пользователя
        response = self.client.post(reverse('users:delete_account'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_save_telegram_id_view(self):
        """
        Проверка сохранения Telegram ID пользователя.

        Убеждается, что переданный Telegram ID сохраняется в профиле пользователя.

        Ожидаемый результат:
            - HTTP статус 200.
            - Telegram ID в профиле обновляется.
        """
        data = {
            'user_id': self.user.id,
            'telegram_id': '987654321'
        }
        response = self.client.post(reverse('users:save_telegram_id'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()  # Обновление данных профиля
        self.assertEqual(self.user.profile.telegram_id, '987654321')  # Проверка обновленного Telegram ID

    def test_get_user_data_view(self):
        """
        Проверка получения данных пользователя по ID.

        Убеждается, что данные пользователя корректно возвращаются в JSON-ответе.

        Ожидаемый результат:
            - HTTP статус 200.
            - JSON-ответ содержит корректные данные пользователя.
        """
        data = {'user_id': self.user.id}
        response = self.client.post(reverse('users:get_user_data'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['username'], self.user.username)  # Проверка корректности возвращаемого username

    def test_get_user_data_by_telegram_id_view(self):
        """
        Проверка получения данных пользователя по Telegram ID.

        Убеждается, что данные пользователя корректно возвращаются в JSON-ответе при передаче Telegram ID.

        Ожидаемый результат:
            - HTTP статус 200.
            - JSON-ответ содержит корректные данные пользователя.
        """
        data = {'telegram_id': self.profile.telegram_id}
        response = self.client.post(reverse('users:get_user_data_by_telegram_id'), data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['user_data']['first_name'], self.user.first_name)  # Проверка возвращаемого first_name

    def test_logout_view(self):
        """
        Проверка выхода пользователя из системы.

        Убеждается, что после выхода пользователя из системы происходит редирект на главную страницу и сеанс завершается.

        Ожидаемый результат:
            - Успешный редирект на главную страницу.
            - Сессия пользователя завершена.
        """
        self.client.login(username='testuser', password='testpassword')  # Авторизация пользователя
        response = self.client.get(reverse('users:logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)  # Проверка завершения сеанса пользователя
