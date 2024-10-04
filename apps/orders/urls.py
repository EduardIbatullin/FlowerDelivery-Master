# apps/orders/urls.py

from django.urls import path  # Импортируем функцию для создания URL-маршрутов

from .views import (
    order_create_view,  # Маршрут для создания нового заказа
    order_history_view,  # Маршрут для просмотра истории заказов пользователя
    cart_detail_view,  # Маршрут для отображения корзины пользователя
    order_summary_view,  # Маршрут для отображения страницы подтверждения заказа
    order_success_view,  # Маршрут для отображения страницы успешного завершения заказа
    update_cart_view,  # Маршрут для обновления корзины
    delete_item_view,  # Маршрут для удаления товаров из корзины
    update_order_item  # Маршрут для изменения количества букетов в корзине
)
from apps.users.views import profile_view  # Импорт представления профиля пользователя

app_name = 'orders'  # Устанавливаем пространство имен для приложения

urlpatterns = [
    path('create/', order_create_view, name='order_create'),  # Страница создания нового заказа
    path('history/', order_history_view, name='order_history'),  # Страница с историей заказов пользователя
    path('cart/', cart_detail_view, name='cart_detail'),  # Страница с корзиной пользователя
    path('summary/', order_summary_view, name='order_summary'),  # Страница подтверждения заказа
    path('success/', order_success_view, name='order_success'),  # Страница успешного завершения заказа
    path('cart/update/', update_cart_view, name='update_cart'),  # Обновление количества товаров в корзине
    path('cart/delete/<int:item_id>/', delete_item_view, name='delete_item'),  # Удаление товара из корзины
    path('profile/', profile_view, name='profile'),  # Профиль пользователя
    path('update_order_item/<int:item_id>/', update_order_item, name='update_order_item'),  # Обновление количества товара в корзине
]

"""
Описание URL-маршрутов:

1. `order_create` — Отображает страницу для создания нового заказа.
   - URL: `/create/`
   - Представление: `order_create_view`.

2. `order_history` — Отображает страницу с историей всех заказов пользователя.
   - URL: `/history/`
   - Представление: `order_history_view`.

3. `cart_detail` — Отображает страницу корзины с текущими товарами пользователя.
   - URL: `/cart/`
   - Представление: `cart_detail_view`.

4. `order_summary` — Страница подтверждения заказа перед его оформлением.
   - URL: `/summary/`
   - Представление: `order_summary_view`.

5. `order_success` — Отображает страницу успешного завершения заказа.
   - URL: `/success/`
   - Представление: `order_success_view`.

6. `update_cart` — Обновляет количество товаров в корзине.
   - URL: `/cart/update/`
   - Представление: `update_cart_view`.

7. `delete_item` — Удаляет выбранный товар из корзины.
   - URL: `/cart/delete/<int:item_id>/`
   - Представление: `delete_item_view`.

8. `profile` — Переход на страницу профиля пользователя.
   - URL: `/profile/`
   - Представление: `profile_view`.

9. `update_order_item` — Обновление количества букетов для элемента заказа.
   - URL: `/update_order_item/<int:item_id>/`
   - Представление: `update_order_item`.
"""
