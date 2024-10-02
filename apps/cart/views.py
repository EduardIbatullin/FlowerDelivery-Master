# apps/cart/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from apps.catalog.models import Product
from .models import Cart, CartItem


# Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product, quantity)

    return redirect('catalog:catalog_list')


# Добавление товара из истории заказов
@login_required
def add_to_cart_from_history(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product, quantity)

    # Перенаправляем обратно на страницу истории заказов после добавления товара
    return redirect('orders:order_history')


@login_required
def cart_detail(request):
    # Создаем корзину для пользователя, если она еще не существует
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'cart': cart,  # Передаем объект корзины в шаблон
    })


def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart:cart_detail')


# Удаление товара из корзины
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    return redirect('cart:cart_detail')
