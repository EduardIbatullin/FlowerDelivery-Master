# apps/analytics/apps.py

from django.apps import AppConfig  # Импорт класса конфигурации приложений Django


class AnalyticsConfig(AppConfig):
    """
    Класс конфигурации приложения аналитики.

    Этот класс используется для настройки и инициализации приложения `analytics`.
    Включает параметры, такие как имя приложения и тип поля по умолчанию.

    Атрибуты:
        - default_auto_field (str): Указывает тип поля для автоматического создания первичного ключа.
        - name (str): Имя приложения, которое используется в Django для его идентификации и настройки.

    Задачи:
        - Конфигурирует приложение аналитики при его инициализации.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.analytics'
