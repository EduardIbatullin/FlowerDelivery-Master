# apps/catalog/views.py

from django.shortcuts import render, get_object_or_404
from .models import Product
from apps.reviews.models import Review
from ..reviews.forms import ReviewForm


def catalog_list_view(request):
    products = Product.objects.all()
    for product in products:
        product.average_rating = product.average_rating()  # Расчет среднего рейтинга

    return render(request, 'catalog/catalog_list.html', {'products': products})


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    product.average_rating = product.average_rating()

    form = ReviewForm()  # Передаем форму для отзыва

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })
