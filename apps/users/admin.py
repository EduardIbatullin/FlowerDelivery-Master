# apps\users\admin.py

from django.contrib import admin  # Импорт базовых инструментов администрирования Django
from django.contrib.auth import get_user_model  # Функция для получения пользовательской модели
from django.contrib.auth.admin import UserAdmin  # Базовый класс админ-панели для модели пользователя

User = get_user_model()  # Получение текущей пользовательской модели пользователя


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомизация административной панели для модели пользователя.

    Этот класс позволяет добавить дополнительные поля или настройки отображения модели пользователя в админ-панели Django.

    Наследуется от:
        UserAdmin: Базовый класс административной панели для пользователя.
    """

    pass  # Место для добавления дополнительных настроек админ-панели
