# apps/management/apps.py

from django.apps import AppConfig  # Импорт базового класса конфигурации приложения Django


class ManagementConfig(AppConfig):
    """
    Конфигурация приложения 'management'.

    Данный класс используется для настройки и регистрации приложения 'management'
    в проекте Django. Он задает основные параметры приложения, такие как его имя
    и тип автоинкрементных полей.

    Атрибуты:
        default_auto_field (str): Тип поля автоинкремента по умолчанию.
        name (str): Имя приложения, которое будет использоваться в проекте.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Установка типа автоинкрементных полей по умолчанию
    name = 'apps.management'  # Имя приложения, которое будет использоваться в проекте
