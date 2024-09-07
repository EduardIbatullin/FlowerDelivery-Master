# apps/orders/urls.py

from django.urls import path
from .views import order_create_view, order_history_view, order_detail_view, cart_detail_view  # Добавляем cart_detail_view

urlpatterns = [
    path('create/', order_create_view, name='order_create'),  # Страница создания заказа
    path('history/', order_history_view, name='order_history'),  # История заказов пользователя
    path('detail/<int:order_id>/', order_detail_view, name='order_detail'),  # Подробности заказа
    path('cart/', cart_detail_view, name='cart_detail'),  # Добавляем маршрут для корзины
]
