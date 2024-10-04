# apps/catalog/apps.py

from django.apps import AppConfig  # Импорт AppConfig для конфигурации приложения


class CatalogConfig(AppConfig):
    """
    Конфигурационный класс для приложения каталога.

    Определяет базовые настройки для приложения `catalog`, такие как имя и
    параметры для полей моделей. Этот класс указывает Django, что приложение
    `catalog` находится в папке `apps.catalog`.

    Атрибуты:
        default_auto_field (str): Указывает тип поля по умолчанию для автоматического создания полей ID.
        name (str): Имя приложения, которое Django использует для регистрации.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.catalog'
