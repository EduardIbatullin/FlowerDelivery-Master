# app/reviews/admin.py

from django.contrib import admin  # Импорт модуля администрирования Django

from .models import Review  # Импорт модели Review для регистрации в админ-панели


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Настраивает отображение модели Review в административной панели Django.

    Этот класс определяет, какие поля отображаются в списке отзывов, по каким полям можно фильтровать и искать отзывы.

    Атрибуты:
        list_display: Кортеж полей, отображаемых в списке отзывов.
        list_filter: Кортеж полей, по которым доступна фильтрация отзывов.
        search_fields: Кортеж полей, по которым осуществляется поиск отзывов.
    """

    list_display = ('product', 'user', 'rating', 'created_at')  # Поля для отображения в списке отзывов
    list_filter = ('product', 'rating', 'created_at')  # Поля для фильтрации списка отзывов
    search_fields = ('user__username', 'product__name')  # Поля для поиска отзывов по связанным моделям
