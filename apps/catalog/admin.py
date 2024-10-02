# apps/catalog/admin.py

from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_available', 'image_preview']
    search_fields = ['name']
    list_filter = ['is_available']

    # Функция для отображения превью изображения в админке
    def image_preview(self, obj):
        if obj.image:
            return '<img src="{}" width="50" height="50" />'.format(obj.image.url)
        return 'Нет изображения'
    image_preview.allow_tags = True
    image_preview.short_description = 'Превью'
