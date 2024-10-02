# apps/management/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from apps.orders.models import Order
from apps.management.forms import OrderStatusForm, OrderFilterForm
from apps.management.models import OrderStatusHistory
import asyncio
from bot.utils import send_telegram_message


User = get_user_model()


@login_required
@user_passes_test(lambda user: user.is_staff)
def order_list_view(request):
    orders = Order.objects.all().order_by('-created_at')
    form = OrderFilterForm(request.GET)

    if form.is_valid():
        status = form.cleaned_data.get('status')
        complete = form.cleaned_data.get('complete')

        if status:
            orders = orders.filter(status=status)
        if complete:
            orders = orders.filter(complete=(complete == 'True'))

    return render(request, 'management/order_list.html', {
        'orders': orders,
        'form': form,
    })


@login_required
@user_passes_test(lambda user: user.is_staff)  # Проверка на то, что пользователь является сотрудником
def order_status_history_view(request, order_id):
    # Получаем заказ по его ID или возвращаем ошибку 404, если он не найден
    order = get_object_or_404(Order, pk=order_id)

    # Получаем историю статусов через OrderStatusHistory с сортировкой по дате изменения
    status_history = OrderStatusHistory.objects.filter(order=order).order_by('-changed_at')

    return render(request, 'management/order_status_history.html', {
        'order': order,
        'status_history': status_history
    })


@login_required
@user_passes_test(lambda user: user.is_staff)
def change_order_status_view(request, order_id):
    # Получаем заказ по ID
    order = get_object_or_404(Order, pk=order_id)
    old_status = order.status

    # Проверяем, была ли нажата кнопка "Снять завершение заказа"
    if 'remove_complete' in request.POST:
        order.complete = False
        order.save()
        messages.success(request, f"Завершение заказа №{order.id} было снято.")
        return redirect('management:change_order_status', order_id=order.id)

    # Проверяем, была ли нажата кнопка "Завершить заказ"
    if 'complete_order' in request.POST:
        order.complete = True
        order.save()
        messages.success(request, f"Заказ №{order.id} был завершен.")
        return redirect('management:change_order_status', order_id=order.id)

    # Инициализируем форму для изменения статуса
    if request.method == 'POST' and 'change_status' in request.POST:
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            new_status = form.cleaned_data['status']

            # Если новый статус совпадает с текущим, не отправляем уведомление и не обновляем
            if new_status != old_status:
                # Обновляем статус заказа
                form.save()

                # Добавляем запись в историю изменений
                OrderStatusHistory.objects.create(
                    order=order,
                    previous_status=old_status,
                    new_status=new_status,
                    changed_by=request.user
                )

                # Отправляем уведомления пользователю и администраторам
                send_order_status_notification(order, old_status, new_status)

                messages.success(request, f"Статус заказа №{order.id} успешно изменен с '{old_status}' на '{new_status}'.")

            return redirect('management:order_list')

    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'management/change_order_status.html', {
        'order': order,
        'form': form
    })


def send_order_status_notification(order, old_status, new_status):
    """
    Отправляет уведомление об изменении статуса заказа пользователю и администраторам.
    """
    user_email = order.user.email
    telegram_id = order.user.profile.telegram_id if hasattr(order.user, 'profile') else None

    # Текст уведомления
    message = (f"Сообщение пользователю {order.user.username} об изменении статуса заказа:\n"
               f"Ваш заказ #{order.id} изменил статус с '{old_status}' на '{new_status}'.\n"
               f"Адрес доставки: {order.delivery_address}\n"
               f"Контактный телефон: {order.contact_phone}")

    # Отправка уведомления по email
    if user_email and order.email_notifications:
        send_mail(
            f"Изменение статуса заказа #{order.id}",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )

    # Отправка уведомления в Telegram
    if telegram_id and order.telegram_notifications:
        asyncio.run(send_telegram_message(telegram_id, message))

    # Отправка уведомлений администраторам

    # Получение администраторов с is_staff=True
    admins = User.objects.filter(is_staff=True)

    # Отправка уведомлений администраторам в Telegram
    for admin in admins:
        admin_telegram_id = admin.profile.telegram_id if hasattr(admin, 'profile') else None
        if admin_telegram_id:
            admin_message = (f"Сообщение администратору магазина {admin.username} об изменении статуса заказа:\n"
                             f"Статус заказа #{order.id} пользователя {order.user.username} "
                             f"изменился с '{old_status}' на '{new_status}'")
            asyncio.run(send_telegram_message(admin_telegram_id, admin_message))


@login_required
@user_passes_test(lambda user: user.is_staff)  # Проверка на то, что пользователь является сотрудником
def order_detail_view(request, order_id):
    # Получаем заказ по его ID
    order = get_object_or_404(Order, pk=order_id)

    # Возвращаем страницу с деталями заказа
    return render(request, 'management/order_detail.html', {'order': order})
