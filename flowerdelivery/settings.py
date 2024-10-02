# flowerdelivery/settings.py

from pathlib import Path
import os
import sys
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Путь к директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Получение переменных окружения
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS').split(',')

# Приложения Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Используемые приложения
    'apps.users',       # Приложение пользователей
    'apps.catalog',     # Приложение каталога
    'apps.orders',      # Приложение заказов
    'apps.reviews',     # Приложение отзывов
    'apps.analytics',   # Приложение аналитики
    'apps.cart',        # Приложение корзины
    'apps.management',  # Приложение управления заказами
    'bot',              # Приложение бота

    # Только если используются
    'django_extensions',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'flowerdelivery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'flowerdelivery' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'flowerdelivery.wsgi.application'

# Настройка базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'TEST': {
            'NAME': 'test_db.sqlite3',
        },
    }
}

if 'test' in sys.argv or os.environ.get('DJANGO_TEST') == 'True':
    DATABASES['default']['NAME'] = 'test_db.sqlite3'

# Настройка аутентификации паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Настройки международных стандартов
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Настройки статических файлов
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Настройки для развёртывания
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/users/login/'
LOGIN_REDIRECT_URL = '/catalog/'
AUTH_USER_MODEL = 'users.CustomUser'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'e.ibatullin@gmail.com'
ADMINS = [('EduardIbatullin', 'e.ibatullin@gmail.com'), ('Admin2', 'admin2@example.com')]

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',  # Используем DEBUG только для отладки
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'filters': ['require_debug_false'],  # Добавляем фильтр
        },
        'console': {
            'level': 'WARNING',  # Ограничиваем вывод консоли до WARNING
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',  # Ограничиваем уровень логирования
            'propagate': True,
        },
        'PIL': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',  # Логируем только ошибки PIL
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',  # Логируем только ошибки SQL-запросов
            'propagate': False,
        },
        '': {  # Для всех остальных
            'handlers': ['file', 'console'],
            'level': 'WARNING',
        },
    },
}
