# apps/management/urls.py

from django.urls import path
from .views import order_list_view, order_status_history_view, change_order_status_view, order_detail_view

app_name = 'management'

urlpatterns = [
    path('orders/', order_list_view, name='order_list'),  # Список заказов
    path('orders/<int:order_id>/status/', change_order_status_view, name='change_order_status'),  # Изменение статуса
    path('orders/<int:order_id>/history/', order_status_history_view, name='order_status_history'),  # История изменений статуса
    path('orders/<int:order_id>/detail/', order_detail_view, name='order_detail'),  # Детали заказа
]
