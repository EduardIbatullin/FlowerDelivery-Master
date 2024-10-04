# flowerdelivery/tests/test_settings.py

from django.conf import settings  # Импорт настроек проекта Django
from django.test import TestCase  # Импорт базового класса для написания тестов


class SettingsTestCase(TestCase):
    """
    Тестовый кейс для проверки настроек проекта в файле settings.py.

    Этот класс включает тесты для проверки наличия и корректности ключевых параметров
    настроек проекта, таких как SECRET_KEY, DEBUG, INSTALLED_APPS, DATABASES и EMAIL_BACKEND.
    """

    def test_secret_key(self):
        """
        Проверка наличия секретного ключа проекта.

        Убеждается, что параметр SECRET_KEY присутствует в настройках и не является None.
        """
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))  # Проверка наличия атрибута SECRET_KEY
        self.assertIsNotNone(settings.SECRET_KEY)  # Убеждение, что SECRET_KEY не равен None

    def test_debug_mode(self):
        """
        Проверка наличия и корректности параметра DEBUG.

        Убеждается, что параметр DEBUG присутствует в настройках.
        """
        self.assertTrue(hasattr(settings, 'DEBUG'))  # Проверка наличия атрибута DEBUG

    def test_installed_apps(self):
        """
        Проверка наличия обязательных приложений в INSTALLED_APPS.

        Проверяет, что стандартные приложения Django присутствуют в списке INSTALLED_APPS.
        """
        required_apps = [
            'django.contrib.admin',  # Админ-панель Django
            'django.contrib.auth',  # Система аутентификации пользователей
            'django.contrib.contenttypes',  # Контент-тип данных для моделей
            'django.contrib.sessions',  # Поддержка сессий
            'django.contrib.messages',  # Система сообщений
            'django.contrib.staticfiles',  # Поддержка статических файлов
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS, f"{app} отсутствует в INSTALLED_APPS")

    def test_database_configuration(self):
        """
        Проверка конфигурации базы данных.

        Убеждается, что конфигурация базы данных задана и использует SQLite.
        """
        self.assertTrue(hasattr(settings, 'DATABASES'))  # Проверка наличия атрибута DATABASES
        self.assertIn('default', settings.DATABASES)  # Проверка наличия ключа 'default' в DATABASES
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3',
                         "Конфигурация базы данных должна использовать SQLite")

    def test_email_configuration(self):
        """
        Проверка настроек email.

        Убеждается, что параметры, связанные с настройкой почтового клиента, присутствуют и корректны.
        """
        self.assertTrue(hasattr(settings, 'EMAIL_BACKEND'))  # Проверка наличия атрибута EMAIL_BACKEND

        # Проверка, что EMAIL_BACKEND установлен в один из допустимых для тестов значений
        allowed_backends = [
            'django.core.mail.backends.console.EmailBackend',  # Почта выводится в консоль (для отладки)
            'django.core.mail.backends.locmem.EmailBackend',   # Почта хранится в памяти (для тестов)
            'django.core.mail.backends.smtp.EmailBackend',     # Отправка почты через SMTP-сервер
        ]
        self.assertIn(settings.EMAIL_BACKEND, allowed_backends,
                      f"Unexpected EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.assertTrue(hasattr(settings, 'DEFAULT_FROM_EMAIL'),
                        "Параметр DEFAULT_FROM_EMAIL должен быть определен в настройках")
