# apps/orders/admin.py

from django.contrib import admin  # Импорт модуля администрирования Django

from .models import Order  # Импорт модели заказов для отображения в админ-панели


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Класс OrderAdmin для настройки отображения и управления заказами в админ-панели Django.

    Определяет, какие поля будут отображаться в списке заказов, добавляет фильтрацию, поиск,
    а также настраивает доступ к полям, которые могут редактироваться в зависимости от статуса заказа.

    Атрибуты:
        list_display (list): Список полей, отображаемых в списке заказов.
        list_filter (list): Фильтры для упрощения поиска заказов.
        search_fields (list): Поля, по которым можно осуществлять поиск.
        readonly_fields (list): Поля, которые не могут быть изменены в админке.
    """
    list_display = ['id', 'user', 'status', 'total_price', 'created_at', 'updated_at']  # Поля для отображения в списке заказов
    list_filter = ['status', 'created_at', 'updated_at']  # Фильтры для упрощения поиска заказов
    search_fields = ['user__username', 'status']  # Поля для поиска (по имени пользователя и статусу заказа)
    readonly_fields = ['created_at', 'updated_at']  # Поля, которые не могут быть изменены в админке

    def get_readonly_fields(self, request, obj=None):
        """
        Метод для ограничения редактирования полей в зависимости от статуса заказа.

        Если заказ имеет статус 'Доставлен' или 'Отменен', то поле 'status' становится только для чтения,
        чтобы предотвратить изменение статуса уже завершенного заказа.

        Параметры:
            request (HttpRequest): Запрос администратора на изменение объекта.
            obj (Order): Экземпляр объекта заказа, если он существует (иначе None).

        Возвращает:
            list: Список полей, которые будут отображаться как только для чтения.
        """
        if obj and obj.status in ['Доставлен', 'Отменен']:
            return self.readonly_fields + ['status']  # Добавляем 'status' к readonly, если заказ завершен
        return self.readonly_fields
