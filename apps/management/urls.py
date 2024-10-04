# apps/management/urls.py

from django.urls import path  # Импорт функции path для определения URL-маршрутов

from .views import (
    order_list_view,  # Импорт представления для отображения списка заказов
    order_status_history_view,  # Импорт представления для отображения истории статусов заказа
    change_order_status_view,  # Импорт представления для изменения статуса заказа
    order_detail_view,  # Импорт представления для отображения детальной информации о заказе
)

# Установка пространства имен для приложения управления заказами
app_name = 'management'

# Определение URL-маршрутов для приложения управления заказами
urlpatterns = [
    path('orders/', order_list_view, name='order_list'),  # Список всех заказов
    path('orders/<int:order_id>/status/', change_order_status_view, name='change_order_status'),  # Изменение статуса заказа
    path('orders/<int:order_id>/history/', order_status_history_view, name='order_status_history'),  # История изменения статуса
    path('orders/<int:order_id>/detail/', order_detail_view, name='order_detail'),  # Детальная информация о заказе
]

"""
Описание URL-маршрутов:

1. `order_list` — Отображает список всех заказов, доступный администраторам для управления.
2. `change_order_status` — Позволяет изменить статус определенного заказа.
3. `order_status_history` — Показывает историю изменения статусов для конкретного заказа.
4. `order_detail` — Показывает детальную информацию о заказе, включая товары, адрес и контактные данные.
"""
