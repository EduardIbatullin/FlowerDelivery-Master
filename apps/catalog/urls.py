# apps/catalog/urls.py

from django.urls import path
from .views import catalog_list_view, product_detail_view

urlpatterns = [
    path('', catalog_list_view, name='catalog_list'),
    path('product/<int:pk>/', product_detail_view, name='product_detail'),
]
