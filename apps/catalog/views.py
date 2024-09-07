# apps/catalog/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product

def catalog_list_view(request):
    products = Product.objects.all()[:16]  # Берем 16 букетов для отображения
    return render(request, 'catalog/catalog_list.html', {'products': products})

def product_detail_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})
