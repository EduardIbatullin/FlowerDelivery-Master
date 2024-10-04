# apps/cart/urls.py

from django.urls import path  # Импорт модуля для создания URL-маршрутов

from . import views  # Импорт представлений приложения корзины

# Установка пространства имен для приложения корзины
app_name = 'cart'

# Определение URL-маршрутов для приложения корзины
urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('update_cart_item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-from-history/<int:product_id>/', views.add_to_cart_from_history, name='add_to_cart_from_history'),
]

"""
Описание URL-маршрутов:

1. `add_to_cart` — Добавляет продукт в корзину на основе переданного идентификатора продукта.
    - Параметры: `<int:product_id>` — ID продукта, который добавляется в корзину.
    - Пример использования: `/add_to_cart/1/` добавляет в корзину продукт с ID 1.

2. `cart_detail` — Отображает страницу с подробной информацией о содержимом корзины.
    - Пример использования: `/cart/` показывает все товары, добавленные в корзину.

3. `update_cart_item` — Обновляет количество конкретного товара в корзине.
    - Параметры: `<int:item_id>` — ID элемента корзины, который нужно обновить.
    - Пример использования: `/update_cart_item/1/` изменяет количество товара с ID 1.

4. `remove_from_cart` — Удаляет товар из корзины на основе идентификатора элемента корзины.
    - Параметры: `<int:item_id>` — ID элемента корзины, который нужно удалить.
    - Пример использования: `/remove_from_cart/1/` удаляет товар с ID 1 из корзины.

5. `add_to_cart_from_history` — Повторное добавление товара в корзину из истории покупок.
    - Параметры: `<int:product_id>` — ID продукта, который нужно добавить в корзину повторно.
    - Пример использования: `/add-from-history/1/` добавляет в корзину продукт с ID 1, ранее купленный пользователем.
"""
