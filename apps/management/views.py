# apps/management/views.py

import asyncio  # Импорт асинхронной библиотеки для отправки уведомлений в Telegram

from django.conf import settings  # Импорт настроек проекта Django
from django.contrib import messages  # Импорт модуля для отображения сообщений пользователю
from django.contrib.auth import get_user_model  # Импорт кастомной модели пользователя
from django.contrib.auth.decorators import login_required, user_passes_test  # Декораторы для ограничения доступа
from django.core.mail import send_mail  # Импорт функции для отправки email
from django.shortcuts import get_object_or_404, redirect, render  # Импорт функций для работы с представлениями

from apps.management.forms import OrderFilterForm, OrderStatusForm  # Импорт форм для управления заказами
from apps.management.models import OrderStatusHistory  # Импорт модели истории статусов заказов
from apps.orders.models import Order  # Импорт модели заказов
from bot.utils import send_telegram_message  # Импорт функции для отправки сообщений в Telegram

# Получение кастомной модели пользователя из настроек
User = get_user_model()  # Получение кастомной модели пользователя из настроек


@login_required
@user_passes_test(lambda user: user.is_staff)  # Ограничение доступа только для сотрудников
def order_list_view(request):
    """
    Представление для отображения списка заказов.
    Доступно только для пользователей со статусом "сотрудник" (is_staff=True).

    Фильтрует заказы на основе переданных параметров, таких как статус заказа и завершенность.

    Аргументы:
        - request: Объект HTTP-запроса.

    Возвращает:
        - HTTP-ответ с рендером страницы 'order_list.html' и контекстом, содержащим заказы и форму фильтрации.
    """
    orders = Order.objects.all().order_by('-created_at')  # Получаем все заказы, отсортированные по дате создания

    form = OrderFilterForm(request.GET)  # Инициализируем форму для фильтрации заказов

    if form.is_valid():  # Применяем фильтры, если форма валидна
        status = form.cleaned_data.get('status')
        complete = form.cleaned_data.get('complete')

        if status:  # Фильтрация по статусу заказа
            orders = orders.filter(status=status)

        if complete:  # Фильтрация по завершенности заказа
            orders = orders.filter(complete=(complete == 'True'))

    return render(request, 'management/order_list.html', {'orders': orders, 'form': form})  # Рендерим страницу


@login_required
@user_passes_test(lambda user: user.is_staff)  # Ограничение доступа только для сотрудников
def order_status_history_view(request, order_id):
    """
    Представление для отображения истории изменения статусов заказа.
    Доступно только для пользователей со статусом "сотрудник" (is_staff=True).

    Аргументы:
        - request: Объект HTTP-запроса.
        - order_id: Идентификатор заказа, для которого нужно показать историю изменений.

    Возвращает:
        - HTTP-ответ с рендером страницы 'order_status_history.html' и контекстом, содержащим заказ и его историю статусов.
    """
    order = get_object_or_404(Order, pk=order_id)  # Получаем заказ по его ID или возвращаем ошибку 404

    status_history = OrderStatusHistory.objects.filter(order=order).order_by('-changed_at')  # Получаем историю изменений

    return render(request, 'management/order_status_history.html', {'order': order, 'status_history': status_history})  # Отображаем страницу


@login_required
@user_passes_test(lambda user: user.is_staff)  # Ограничение доступа только для сотрудников
def change_order_status_view(request, order_id):
    """
    Представление для изменения статуса заказа.
    Доступно только для пользователей со статусом "сотрудник" (is_staff=True).

    Аргументы:
        - request: Объект HTTP-запроса.
        - order_id: Идентификатор заказа, статус которого нужно изменить.

    Возвращает:
        - HTTP-ответ с рендером страницы 'change_order_status.html' с формой для изменения статуса заказа.
    """
    order = get_object_or_404(Order, pk=order_id)  # Получаем заказ по его ID или возвращаем ошибку 404
    old_status = order.status  # Сохраняем старый статус заказа

    if 'remove_complete' in request.POST:  # Обработка нажатия кнопки "Снять завершение заказа"
        order.complete = False
        order.save()
        messages.success(request, f"Завершение заказа №{order.id} было снято.")
        return redirect('management:change_order_status', order_id=order.id)

    if 'complete_order' in request.POST:  # Обработка нажатия кнопки "Завершить заказ"
        order.complete = True
        order.save()
        messages.success(request, f"Заказ №{order.id} был завершен.")
        return redirect('management:change_order_status', order_id=order.id)

    if request.method == 'POST' and 'change_status' in request.POST:  # Обработка изменения статуса через форму
        form = OrderStatusForm(request.POST, instance=order)  # Инициализируем форму с текущими данными
        if form.is_valid():
            new_status = form.cleaned_data['status']

            if new_status != old_status:  # Проверяем, отличается ли новый статус от старого
                form.save()  # Сохраняем новый статус заказа

                OrderStatusHistory.objects.create(  # Сохраняем изменения в истории статусов
                    order=order,
                    previous_status=old_status,
                    new_status=new_status,
                    changed_by=request.user
                )

                send_order_status_notification(order, old_status, new_status)  # Отправляем уведомление о смене статуса

                messages.success(request, f"Статус заказа №{order.id} успешно изменен с '{old_status}' на '{new_status}'.")
            return redirect('management:order_list')

    else:  # Инициализируем форму, если запрос не POST
        form = OrderStatusForm(instance=order)

    return render(request, 'management/change_order_status.html', {'order': order, 'form': form})  # Рендерим страницу


def send_order_status_notification(order, old_status, new_status):
    """
    Отправляет уведомление об изменении статуса заказа пользователю и администраторам.

    Аргументы:
        - order: Объект заказа, статус которого был изменен.
        - old_status: Предыдущий статус заказа.
        - new_status: Новый статус заказа.
    """
    user_email = order.user.email
    telegram_id = order.user.profile.telegram_id if hasattr(order.user, 'profile') else None

    message = (  # Формируем текст уведомления для пользователя
        f"Сообщение пользователю {order.user.username} об изменении статуса заказа:\n"
        f"Ваш заказ #{order.id} изменил статус с '{old_status}' на '{new_status}'.\n"
        f"Адрес доставки: {order.delivery_address}\n"
        f"Контактный телефон: {order.contact_phone}"
    )

    if user_email and order.email_notifications:  # Отправляем уведомление по email
        send_mail(
            f"Изменение статуса заказа #{order.id}",
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )

    if telegram_id and order.telegram_notifications:  # Отправляем уведомление в Telegram
        asyncio.run(send_telegram_message(telegram_id, message))

    admins = User.objects.filter(is_staff=True)  # Получаем всех администраторов

    for admin in admins:  # Отправляем уведомления в Telegram администраторам
        admin_telegram_id = admin.profile.telegram_id if hasattr(admin, 'profile') else None
        if admin_telegram_id:
            admin_message = (
                f"Сообщение администратору магазина {admin.username} об изменении статуса заказа:\n"
                f"Статус заказа #{order.id} пользователя {order.user.username} изменился с '{old_status}' на '{new_status}'."
            )
            asyncio.run(send_telegram_message(admin_telegram_id, admin_message))


@login_required
@user_passes_test(lambda user: user.is_staff)  # Ограничение доступа только для сотрудников
def order_detail_view(request, order_id):
    """
    Представление для отображения деталей заказа.
    Доступно только для пользователей со статусом "сотрудник" (is_staff=True).

    Аргументы:
        - request: Объект HTTP-запроса.
        - order_id: Идентификатор заказа, для которого нужно показать детали.

    Возвращает:
        - HTTP-ответ с рендером страницы 'order_detail.html' и контекстом, содержащим детали заказа.
    """
    order = get_object_or_404(Order, pk=order_id)  # Получаем заказ по его ID или возвращаем ошибку 404

    return render(request, 'management/order_detail.html', {'order': order})  # Рендерим страницу
