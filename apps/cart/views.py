# apps/cart/views.py

from django.contrib.auth.decorators import login_required  # Импорт декоратора для ограничения доступа к представлениям только для авторизованных пользователей
from django.shortcuts import get_object_or_404, redirect, render  # Импорт функций для получения объекта, перенаправления и рендеринга шаблонов

from apps.catalog.models import Product  # Импорт модели Product для работы с товарами каталога
from .models import Cart, CartItem  # Импорт моделей Cart и CartItem для работы с корзиной пользователя


@login_required
def add_to_cart(request, product_id):
    """
    Добавление товара в корзину.

    Если у пользователя нет корзины, она создается автоматически. Затем продукт
    добавляется в корзину с указанным количеством.

    Аргументы:
        - request: Объект HTTP-запроса.
        - product_id (int): Идентификатор продукта, который добавляется в корзину.

    Действие:
        - Добавляет продукт в корзину пользователя. Если продукт уже в корзине, увеличивает его количество.

    Возвращает:
        - Перенаправляет на страницу каталога после добавления продукта.
    """
    product = get_object_or_404(Product, pk=product_id)  # Получаем объект продукта по ID или возвращаем 404, если не найден
    quantity = int(request.POST.get('quantity', 1))  # Получаем количество из POST-запроса или устанавливаем 1 по умолчанию

    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product, quantity)  # Добавляем продукт в корзину

    return redirect('catalog:catalog_list')  # Перенаправление на страницу каталога


@login_required
def add_to_cart_from_history(request, product_id):
    """
    Добавление товара в корзину из истории покупок.

    Позволяет пользователю повторно добавить продукт в корзину из истории его заказов.

    Аргументы:
        - request: Объект HTTP-запроса.
        - product_id (int): Идентификатор продукта, который добавляется в корзину.

    Действие:
        - Добавляет продукт в корзину пользователя с указанным количеством.

    Возвращает:
        - Перенаправляет на страницу истории заказов после добавления продукта.
    """
    product = get_object_or_404(Product, pk=product_id)  # Получаем объект продукта по ID или возвращаем 404, если не найден
    quantity = int(request.POST.get('quantity', 1))  # Получаем количество из POST-запроса или устанавливаем 1 по умолчанию

    # Получаем или создаем корзину для пользователя
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.add_product(product, quantity)  # Добавляем продукт в корзину

    return redirect('orders:order_history')  # Перенаправление на страницу истории заказов


@login_required
def cart_detail(request):
    """
    Отображение содержимого корзины пользователя.

    Если корзины еще нет, она создается автоматически. Отображает все товары,
    добавленные в корзину.

    Аргументы:
        - request: Объект HTTP-запроса.

    Возвращает:
        - Шаблон `cart/cart_detail.html` с контекстом:
            - `cart_items`: Список элементов в корзине.
            - `cart`: Объект корзины.
    """
    # Создаем корзину для пользователя, если она еще не существует
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()  # Получаем все элементы корзины

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,  # Передаем элементы корзины в шаблон
        'cart': cart,  # Передаем объект корзины в шаблон
    })


@login_required
def update_cart_item(request, item_id):
    """
    Обновление количества конкретного элемента в корзине.

    Позволяет пользователю изменить количество конкретного товара в его корзине.

    Аргументы:
        - request: Объект HTTP-запроса.
        - item_id (int): Идентификатор элемента корзины, количество которого нужно изменить.

    Действие:
        - Обновляет количество указанного элемента корзины.

    Возвращает:
        - Перенаправляет на страницу корзины (`cart:cart_detail`) после обновления количества.
    """
    cart_item = get_object_or_404(CartItem, pk=item_id)  # Получаем элемент корзины или возвращаем 404, если не найден
    quantity = int(request.POST.get('quantity', 1))  # Получаем новое количество из POST-запроса
    cart_item.quantity = quantity  # Обновляем количество элемента
    cart_item.save()  # Сохраняем изменения

    return redirect('cart:cart_detail')  # Перенаправление на страницу корзины


@login_required
def remove_from_cart(request, item_id):
    """
    Удаление товара из корзины.

    Позволяет пользователю удалить конкретный товар из его корзины.

    Аргументы:
        - request: Объект HTTP-запроса.
        - item_id (int): Идентификатор элемента корзины, который нужно удалить.

    Действие:
        - Удаляет элемент корзины.

    Возвращает:
        - Перенаправляет на страницу корзины (`cart:cart_detail`) после удаления элемента.
    """
    cart_item = get_object_or_404(CartItem, pk=item_id)  # Получаем элемент корзины или возвращаем 404, если не найден
    cart_item.delete()  # Удаляем элемент корзины
    return redirect('cart:cart_detail')  # Перенаправление на страницу корзины
