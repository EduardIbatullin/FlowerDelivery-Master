from django.urls import path
from .views import (
    order_create_view,  # Маршрут для создания заказа
    order_history_view,  # Маршрут для истории заказов
    cart_detail_view,  # Маршрут для корзины
    order_summary_view,  # Маршрут для подтверждения заказа
    order_success_view,  # Маршрут для успешного завершения заказа
    update_cart_view,  # Маршрут для обновления корзины
    delete_item_view,   # Маршрут для удаления товаров из корзины
    update_order_item  # Маршрут для изменения количества букетов
)
from apps.users.views import profile_view

app_name = 'orders'

urlpatterns = [
    path('create/', order_create_view, name='order_create'),  # Страница создания заказа
    path('history/', order_history_view, name='order_history'),  # История заказов пользователя
    # path('detail/<int:order_id>/', order_detail_view, name='order_detail'),  # Подробности заказа
    path('cart/', cart_detail_view, name='cart_detail'),  # Маршрут для корзины
    path('summary/', order_summary_view, name='order_summary'),  # Маршрут для подтверждения заказа
    path('success/', order_success_view, name='order_success'),  # Страница успешного завершения заказа
    path('cart/update/', update_cart_view, name='update_cart'),  # Маршрут для обновления количества товаров
    path('cart/delete/<int:item_id>/', delete_item_view, name='delete_item'),  # Маршрут для удаления товаров
    path('profile/', profile_view, name='profile'),  # Профиль пользователя
    path('update_order_item/<int:item_id>/', update_order_item, name='update_order_item'),  # Обновление количества
]
