# apps/orders/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm


def order_create_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_history')
    else:
        form = OrderForm()
    return render(request, 'orders/order_create.html', {'form': form})


@login_required  # Декоратор, чтобы убедиться, что пользователь аутентифицирован
def order_history_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required  # Декоратор, чтобы убедиться, что пользователь аутентифицирован
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})


def cart_detail_view(request):
    # Логика отображения корзины
    cart_items = []  # Реализуйте получение товаров в корзине
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})
