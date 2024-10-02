# apps/orders/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
# from django.core.mail import send_mail
# from django.conf import settings
import asyncio
from datetime import datetime
from .models import Order, OrderItem
from .forms import OrderForm
from apps.cart.models import Cart, CartItem
from apps.users.models import Profile
from bot.utils import send_telegram_message


User = get_user_model()


@login_required
def order_create_view(request):
    """
    Обрабатывает процесс создания заказа.
    Пользователь выбирает товары и заполняет данные для доставки.
    """
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()

    try:
        user_profile = request.user.profile
    except Profile.DoesNotExist:
        user_profile = None

    has_email = bool(user_profile and user_profile.email)
    has_telegram = bool(user_profile and user_profile.telegram_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if 'submit_order' in request.POST:
            if form.is_valid():
                # Сохраняем информацию о заказе в сессии, а не в БД
                request.session['order_data'] = {
                    'delivery_address': form.cleaned_data['delivery_address'],
                    'contact_phone': form.cleaned_data['contact_phone'],
                    'delivery_date': form.cleaned_data['delivery_date'].strftime('%Y-%m-%d'),
                    'delivery_time': form.cleaned_data['delivery_time'].strftime('%H:%M'),
                    'additional_info': form.cleaned_data['additional_info'],
                    'email_notifications': user_profile.email if 'email_notifications' in request.POST else None,
                    'telegram_notifications': user_profile.telegram_id if 'telegram_notifications' in request.POST else None
                }

                # Переход на страницу подтверждения заказа
                return redirect('orders:order_summary')

            else:
                return render(request, 'orders/order_create.html', {
                    'form': form,
                    'cart_items': cart_items,
                    'total_price': total_price,
                    'user_profile': user_profile,
                    'has_email': has_email,
                    'has_telegram': has_telegram,
                    'form_errors': form.errors
                })

    else:
        # Если данные заказа уже есть в сессии, заполняем форму
        if 'order_data' in request.session:
            order_data = request.session['order_data']
            form = OrderForm(initial={
                'delivery_address': order_data.get('delivery_address', ''),
                'contact_phone': order_data.get('contact_phone', ''),
                'delivery_date': order_data.get('delivery_date', ''),
                'delivery_time': order_data.get('delivery_time', ''),
                'additional_info': order_data.get('additional_info', ''),
                'email_notifications': order_data.get('email_notifications', ''),
                'telegram_notifications': order_data.get('telegram_notifications', ''),
            })
        else:
            form = OrderForm()

    return render(request, 'orders/order_create.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'user_profile': user_profile,
        'has_email': has_email,
        'has_telegram': has_telegram
    })


@login_required
def update_cart_view(request):
    """
    Обрабатывает изменение количества товаров в корзине.
    """
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                product_id = key.split('_')[1]
                quantity = int(value)
                cart_item = cart.items.get(product_id=product_id)
                cart_item.quantity = quantity
                cart_item.save()
        return redirect('orders:order_create')


@login_required
def delete_item_view(request, item_id):
    """
    Удаляет товар из корзины пользователя.
    """
    cart = Cart.objects.get(user=request.user)
    cart_item = cart.items.get(id=item_id)
    cart_item.delete()
    return redirect('orders:order_create')


@login_required
def order_summary_view(request):
    """
    Отображает страницу с подтверждением заказа, где пользователь может окончательно подтвердить или изменить заказ.
    """
    if 'order_data' not in request.session:
        return redirect('orders:order_create')

    order_data = request.session['order_data']
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()

    no_notifications = not (order_data.get('email_notifications') or order_data.get('telegram_notifications'))

    if request.method == 'POST':
        if 'confirm_order' in request.POST:
            # Создаем и сохраняем заказ в БД только после подтверждения
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                delivery_address=order_data['delivery_address'],
                contact_phone=order_data['contact_phone'],
                delivery_date=order_data['delivery_date'],
                delivery_time=order_data['delivery_time'],
                additional_info=order_data.get('additional_info', ''),
                email_notifications=bool(order_data.get('email_notifications', False)),
                telegram_notifications=bool(order_data.get('telegram_notifications', False))
            )

            # Добавляем товары в заказ через OrderItem
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price_at_purchase=item.product.price  # сохраняем цену на момент покупки
                )

            # Отправляем уведомления, если выбран способ
            send_order_notifications(order)

            # Очищаем корзину пользователя
            cart.items.all().delete()

            # Очищаем сессию после завершения заказа
            del request.session['order_data']

            return redirect('orders:order_success')

        if 'edit_order' in request.POST:
            # Возвращаемся на страницу создания заказа для редактирования
            return redirect('orders:order_create')

    return render(request, 'orders/order_summary.html', {
        'order_data': order_data,
        'cart_items': cart_items,
        'total_price': total_price,
        'no_notifications': no_notifications
    })


def send_order_notifications(order):
    """
    Отправляет уведомления по Telegram пользователю и администраторам при подтверждении заказа.
    """
    # Преобразуем строки даты и времени в объекты datetime
    delivery_date = datetime.strptime(order.delivery_date, '%Y-%m-%d')
    delivery_time = datetime.strptime(order.delivery_time, '%H:%M')

    # Формирование списка товаров из OrderItem
    items = ', '.join([f'букет {item.product.name} - {item.quantity} шт.' for item in order.items.all()])

    # Сообщение для пользователя
    user_message = (f"Сообщение пользователю {order.user.username}.\n"
                    f"Вы сделали заказ в магазине цветов и букетов Classic Floral Shop.\n"
                    f"Номер вашего заказа: {order.id}\n"
                    f"Общая стоимость: {order.total_price:.2f} руб.\n"
                    f"Детали заказа:\n"
                    f"Адрес доставки: {order.delivery_address}\n"
                    f"Контактный телефон: {order.contact_phone}\n"
                    f"Дата доставки: {delivery_date:%d-%m-%Y}\n" 
                    f"Время доставки: {delivery_time:%H:%M}\n" 
                    f"Дополнительная информация: {order.additional_info}\n"
                    f"Товары: {items}")

    # Отправка уведомления в Telegram пользователю
    if order.telegram_notifications:
        telegram_id = order.user.profile.telegram_id if hasattr(order.user, 'profile') else None
        if telegram_id:
            asyncio.run(send_telegram_message(telegram_id, user_message))

    # Получение списка администраторов (is_staff=True)
    admins = User.objects.filter(is_staff=True)

    # Отправка уведомлений администраторам в Telegram
    for admin in admins:
        admin_telegram_id = admin.profile.telegram_id if hasattr(admin, 'profile') else None
        if admin_telegram_id:
            admin_message = (f"Сообщение администратору магазина {admin.username}:\n"
                             f"Новый заказ #{order.id} от {order.user.username}.\n"
                             f"Общая стоимость: {order.total_price:.2f} руб.\n"
                             f"Адрес доставки: {order.delivery_address}\n"
                             f"Дата доставки: {delivery_date:%d-%m-%Y}\n"  # Используем объекты datetime для форматирования
                             f"Товары: {items}")
            asyncio.run(send_telegram_message(admin_telegram_id, admin_message))


@login_required
def order_history_view(request):
    """
    Отображает историю заказов пользователя.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_success_view(request):
    """
    Отображает страницу успешного завершения заказа.
    Очищает сессию от данных заказа.
    """
    request.session.pop('order_data', None)  # Удаление данных о заказе из сессии
    return render(request, 'orders/order_success.html')


def cart_detail_view(request):
    """
    Отображает содержимое корзины пользователя.
    """
    cart_items = []  # Здесь будет логика отображения корзины
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})


@login_required
def update_order_item(request, item_id):
    """
    Обработчик для изменения количества букетов на странице "Оформления заказа".
    """
    order_item = get_object_or_404(OrderItem, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        order_item.quantity = quantity
        order_item.save()  # Убедитесь, что изменения сохраняются
    else:
        order_item.delete()  # Удаляем элемент заказа, если количество меньше 1

    # Оставляем пользователя на странице "Оформления заказа" после обновления количества
    return redirect('orders:order_create')
