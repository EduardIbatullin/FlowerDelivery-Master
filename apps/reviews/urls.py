# apps/reviews/urls.py

from django.urls import path  # Импорт функции path для определения маршрутов URL-адресов
from . import views  # Импорт представлений из текущего приложения

app_name = 'reviews'  # Установка пространства имен для приложения

urlpatterns = [
    path('add/<int:product_id>/', views.add_review, name='add_review'),  # Маршрут для добавления нового отзыва к продукту
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),  # Маршрут для редактирования существующего отзыва
]

"""
Описание URL-маршрутов:

1. `add_review` — Отображает страницу для добавления нового отзыва к выбранному продукту.
   - URL: `/add/<int:product_id>/`
   - Представление: `views.add_review`
   - Аргументы:
     - `product_id`: Идентификатор продукта, к которому добавляется отзыв.

2. `edit_review` — Отображает страницу для редактирования существующего отзыва пользователя.
   - URL: `/edit/<int:review_id>/`
   - Представление: `views.edit_review`
   - Аргументы:
     - `review_id`: Идентификатор отзыва, который необходимо отредактировать.
"""
