# apps/orders/admin.py

from django.contrib import admin
from .models import Order  # Импортируем модель заказов


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'status', 'total_price', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'status']
    readonly_fields = ['created_at', 'updated_at']  # Эти поля только для чтения

    # Настраиваем возможность изменения статуса заказа
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.status in ['Доставлен', 'Отменен']:
            return self.readonly_fields + ['status']  # Нельзя менять статус если заказ завершен
        return self.readonly_fields
