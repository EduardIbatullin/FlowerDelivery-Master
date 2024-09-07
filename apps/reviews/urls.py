from django.urls import path
from .views import review_list_view, review_create_view

urlpatterns = [
    path('product/<int:product_id>/', review_list_view, name='review_list'),  # Просмотр отзывов для продукта
    path('product/<int:product_id>/add/', review_create_view, name='review_create'),  # Добавление отзыва
]
