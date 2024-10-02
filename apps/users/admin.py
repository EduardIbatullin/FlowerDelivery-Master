# apps\users\admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Здесь можно добавить дополнительные поля или настройки админки для пользователя
    pass
