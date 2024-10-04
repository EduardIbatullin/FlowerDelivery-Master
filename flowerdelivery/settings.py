# flowerdelivery/settings.py

from pathlib import Path  # Импортируем Path для работы с путями
import os  # Импортируем os для работы с переменными окружения и файловой системой
import sys  # Импортируем sys для доступа к аргументам командной строки
from dotenv import load_dotenv  # Импортируем библиотеку для загрузки переменных окружения из .env файла

# Загрузка переменных окружения из .env файла
load_dotenv()

# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Получение переменных окружения
SECRET_KEY = os.getenv('SECRET_KEY')  # Секретный ключ для криптографических операций
DEBUG = os.getenv('DEBUG') == 'True'  # Установка режима отладки на основе переменной окружения
# Разрешенные хосты зависят от режима отладки
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS').split(',')

# Определение установленных приложений Django
INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Приложения проекта
    'apps.users',       # Приложение для управления пользователями
    'apps.catalog',     # Приложение каталога товаров
    'apps.orders',      # Приложение для управления заказами
    'apps.reviews',     # Приложение отзывов пользователей
    'apps.analytics',   # Приложение для аналитики
    'apps.cart',        # Приложение корзины покупок
    'apps.management',  # Приложение управления заказами
    'bot',              # Приложение Telegram-бота

    # Сторонние приложения (если используются)
    'django_extensions',  # Дополнительные команды и утилиты для разработки
    'rest_framework',     # Фреймворк для создания RESTful API
]

# Определение промежуточного ПО (Middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Защита от веб-атак
    'django.contrib.sessions.middleware.SessionMiddleware',  # Управление сессиями
    'django.middleware.common.CommonMiddleware',  # Общие настройки
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация
    'django.contrib.messages.middleware.MessageMiddleware',  # Управление сообщениями
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от кликджекинга
]

# Корневой конфигурационный файл URL
ROOT_URLCONF = 'flowerdelivery.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Используем движок Django для рендеринга шаблонов
        'DIRS': [BASE_DIR / 'flowerdelivery' / 'templates'],  # Путь к пользовательским шаблонам
        'APP_DIRS': True,  # Автоматический поиск шаблонов в папках приложений
        'OPTIONS': {
            'context_processors': [  # Список процессоров контекста
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение для развертывания
WSGI_APPLICATION = 'flowerdelivery.wsgi.application'

# Конфигурация базы данных (SQLite используется по умолчанию)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Используем SQLite
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Имя файла базы данных
        'TEST': {
            'NAME': 'test_db.sqlite3',  # Имя базы данных для тестов
        },
    }
}

# Если тестирование, используем тестовую базу данных
if 'test' in sys.argv or os.environ.get('DJANGO_TEST') == 'True':
    DATABASES['default']['NAME'] = 'test_db.sqlite3'

# Настройки аутентификации паролей (минимальные требования)
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Локализация и временные зоны
LANGUAGE_CODE = 'ru-ru'  # Устанавливаем язык на русский
TIME_ZONE = 'UTC'  # Устанавливаем временную зону на UTC
USE_I18N = True  # Включаем международные стандарты
USE_L10N = True  # Включаем локализацию
USE_TZ = True  # Включаем поддержку временных зон

# Настройки статических файлов (CSS, JavaScript и изображения)
STATIC_URL = '/static/'  # URL для статических файлов
STATICFILES_DIRS = [BASE_DIR / "static"]  # Папка для поиска статических файлов
MEDIA_URL = '/media/'  # URL для медиа-файлов
MEDIA_ROOT = BASE_DIR / "media"  # Папка для хранения медиа-файлов
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для статических файлов при сборке

# Автоматическое поле первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки аутентификации и редиректов
LOGIN_URL = '/users/login/'  # URL для страницы логина
LOGIN_REDIRECT_URL = '/catalog/'  # URL для редиректа после успешного логина
LOGOUT_REDIRECT_URL = '/'  # URL для редиректа после выхода из системы
AUTH_USER_MODEL = 'users.CustomUser'  # Пользовательская модель пользователя

# Настройки почты (используем консольный бэкенд)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'e.ibatullin@gmail.com'  # Почта по умолчанию для отправки писем
ADMINS = [('EduardIbatullin', 'e.ibatullin@gmail.com'), ('Admin2', 'admin2@example.com')]  # Администраторы

# Конфигурация логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'file': {  # Логирование в файл
            'level': 'DEBUG',  # Уровень отладки
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',  # Путь к лог-файлу
            'filters': ['require_debug_false'],  # Фильтр для логирования только вне режима отладки
        },
        'console': {  # Логирование в консоль
            'level': 'WARNING',  # Логируем только предупреждения и ошибки
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],  # Логгеры Django
            'level': 'WARNING',
            'propagate': True,
        },
        'PIL': {  # Логгеры для работы с изображениями
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {  # Логгеры для базы данных
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        '': {  # Все остальные логгеры
            'handlers': ['file', 'console'],
            'level': 'WARNING',
        },
    },
}
