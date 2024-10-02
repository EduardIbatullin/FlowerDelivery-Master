# flowerdelivery/tests/test_settings.py

from django.conf import settings
from django.test import TestCase


class SettingsTestCase(TestCase):
    """Тестирование файла настроек settings.py"""

    def test_secret_key(self):
        """Проверка наличия секретного ключа"""
        self.assertTrue(hasattr(settings, 'SECRET_KEY'))
        self.assertIsNotNone(settings.SECRET_KEY)

    def test_debug_mode(self):
        """Проверка режима DEBUG"""
        self.assertTrue(hasattr(settings, 'DEBUG'))

    def test_installed_apps(self):
        """Проверка наличия обязательных приложений"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_database_configuration(self):
        """Проверка конфигурации базы данных"""
        self.assertTrue(hasattr(settings, 'DATABASES'))
        self.assertIn('default', settings.DATABASES)
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

    def test_email_configuration(self):
        """Проверка настроек email"""
        self.assertTrue(hasattr(settings, 'EMAIL_BACKEND'))

        # Проверка, что EMAIL_BACKEND установлен в один из допустимых для тестов значений
        allowed_backends = [
            'django.core.mail.backends.console.EmailBackend',
            'django.core.mail.backends.locmem.EmailBackend',
            'django.core.mail.backends.smtp.EmailBackend',
        ]
        self.assertIn(settings.EMAIL_BACKEND, allowed_backends, f"Unexpected EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        self.assertTrue(hasattr(settings, 'DEFAULT_FROM_EMAIL'))
