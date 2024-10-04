# apps/users/tests/test_urls.py

from django.test import SimpleTestCase  # Импорт базового класса для создания простых тестов Django
from django.urls import reverse, resolve  # Импорт функций для работы с URL-маршрутами
from apps.users.views import (  # Импортируем представления, используемые для проверки разрешений URL-адресов
    CustomLoginView,
    logout_view,
    register_view,
    profile_view,
    edit_profile_view,
    register_bot,
    delete_account,
    save_telegram_id,
    get_user_data,
    get_user_data_by_telegram_id
)


class UsersUrlsTest(SimpleTestCase):
    """
    Набор тестов для проверки разрешения URL-маршрутов приложения `users`.

    Тестируемые сценарии:
    1. Проверка разрешения URL для каждого представления.
    """

    def test_login_url_resolves(self):
        """
        Проверка разрешения URL для страницы входа пользователя.

        Убеждается, что URL для страницы входа соответствует представлению `CustomLoginView`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с классом представления `CustomLoginView`.
        """
        url = reverse('users:login')  # Получаем URL для маршрута 'login'
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)  # Проверяем соответствие URL и представления

    def test_logout_url_resolves(self):
        """
        Проверка разрешения URL для страницы выхода пользователя.

        Убеждается, что URL для выхода пользователя соответствует представлению `logout_view`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `logout_view`.
        """
        url = reverse('users:logout')  # Получаем URL для маршрута 'logout'
        self.assertEqual(resolve(url).func, logout_view)  # Проверяем соответствие URL и представления

    def test_register_url_resolves(self):
        """
        Проверка разрешения URL для страницы регистрации.

        Убеждается, что URL для регистрации пользователя соответствует представлению `register_view`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `register_view`.
        """
        url = reverse('users:register')  # Получаем URL для маршрута 'register'
        self.assertEqual(resolve(url).func, register_view)  # Проверяем соответствие URL и представления

    def test_profile_url_resolves(self):
        """
        Проверка разрешения URL для страницы профиля пользователя.

        Убеждается, что URL для профиля пользователя соответствует представлению `profile_view`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `profile_view`.
        """
        url = reverse('users:profile')  # Получаем URL для маршрута 'profile'
        self.assertEqual(resolve(url).func, profile_view)  # Проверяем соответствие URL и представления

    def test_edit_profile_url_resolves(self):
        """
        Проверка разрешения URL для страницы редактирования профиля пользователя.

        Убеждается, что URL для редактирования профиля пользователя соответствует представлению `edit_profile_view`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `edit_profile_view`.
        """
        url = reverse('users:edit_profile')  # Получаем URL для маршрута 'edit_profile'
        self.assertEqual(resolve(url).func, edit_profile_view)  # Проверяем соответствие URL и представления

    def test_register_bot_url_resolves(self):
        """
        Проверка разрешения URL для регистрации в Telegram-боте.

        Убеждается, что URL для регистрации в боте соответствует представлению `register_bot`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `register_bot`.
        """
        url = reverse('users:register_bot')  # Получаем URL для маршрута 'register_bot'
        self.assertEqual(resolve(url).func, register_bot)  # Проверяем соответствие URL и представления

    def test_delete_account_url_resolves(self):
        """
        Проверка разрешения URL для удаления аккаунта пользователя.

        Убеждается, что URL для удаления аккаунта пользователя соответствует представлению `delete_account`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `delete_account`.
        """
        url = reverse('users:delete_account')  # Получаем URL для маршрута 'delete_account'
        self.assertEqual(resolve(url).func, delete_account)  # Проверяем соответствие URL и представления

    def test_save_telegram_id_url_resolves(self):
        """
        Проверка разрешения URL для сохранения Telegram ID пользователя.

        Убеждается, что URL для сохранения Telegram ID соответствует представлению `save_telegram_id`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `save_telegram_id`.
        """
        url = reverse('users:save_telegram_id')  # Получаем URL для маршрута 'save_telegram_id'
        self.assertEqual(resolve(url).func, save_telegram_id)  # Проверяем соответствие URL и представления

    def test_get_user_data_url_resolves(self):
        """
        Проверка разрешения URL для получения данных пользователя.

        Убеждается, что URL для получения данных пользователя соответствует представлению `get_user_data`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `get_user_data`.
        """
        url = reverse('users:get_user_data')  # Получаем URL для маршрута 'get_user_data'
        self.assertEqual(resolve(url).func, get_user_data)  # Проверяем соответствие URL и представления

    def test_get_user_data_by_telegram_id_url_resolves(self):
        """
        Проверка разрешения URL для получения данных пользователя по Telegram ID.

        Убеждается, что URL для получения данных по Telegram ID соответствует представлению `get_user_data_by_telegram_id`.

        Ожидаемый результат:
            - Разрешенный URL сопоставляется с функцией `get_user_data_by_telegram_id`.
        """
        url = reverse('users:get_user_data_by_telegram_id')  # Получаем URL для маршрута 'get_user_data_by_telegram_id'
        self.assertEqual(resolve(url).func, get_user_data_by_telegram_id)  # Проверяем соответствие URL и представления
