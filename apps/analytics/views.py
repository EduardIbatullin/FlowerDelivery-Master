# apps/analytics/views.py

import json  # Импорт модуля для работы с JSON-данными

from django.contrib import messages  # Импорт для управления сообщениями в интерфейсе
from django.contrib.auth import get_user_model  # Импорт для получения модели пользователя
from django.contrib.auth.decorators import login_required, user_passes_test  # Импорт декораторов для проверки прав доступа
from django.db import models  # Импорт модуля для работы с моделями и базой данных
from django.http import JsonResponse  # Импорт модуля для формирования JSON-ответов
from django.shortcuts import render, redirect  # Импорт методов для отображения и перенаправления
from django.utils import timezone  # Импорт модуля для работы с временными данными
from django.views.decorators.csrf import csrf_exempt  # Импорт декоратора для отключения проверки CSRF

from apps.users.models import Profile  # Импорт модели профиля пользователя
from .forms import AnalyticsFilterForm  # Импорт формы фильтрации данных аналитики
from .models import SalesAnalytics  # Импорт модели аналитики продаж
from .utils import update_analytics_data  # Импорт функции обновления аналитики

# Получение модели пользователя из текущей конфигурации проекта
User = get_user_model()


@login_required
@user_passes_test(lambda user: user.is_staff)
def analytics_dashboard(request):
    """
    Отображает панель аналитики с фильтрацией по периодам и продуктам.

    Функция отображает страницу с аналитическими данными, включая общее количество заказов, выручку
    и динамику продаж. Данные можно фильтровать по периоду времени и конкретным букетам.

    Порядок работы:
    1. Инициализация формы фильтрации с предустановленными вариантами периода времени.
    2. Обработка данных формы и определение временного диапазона для фильтрации.
    3. Сбор и группировка данных аналитики на основе выбранного периода и продукта.
    4. Подготовка контекста с данными и графиками для отображения на странице.

    Аргументы:
        request (HttpRequest): Объект запроса, содержащий GET-параметры для фильтрации и данные сеанса пользователя.

    Возвращает:
        HttpResponse: Шаблон `analytics_dashboard.html`, отображающий данные аналитики и графики.
    """
    form = AnalyticsFilterForm(request.GET or None)

    # Инициализация параметров фильтрации по умолчанию
    period_start = None
    period_end = None
    product = None

    # Обработка данных из формы, если они валидны
    if form.is_valid():
        period = form.cleaned_data['period']
        product = form.cleaned_data['product']

        # Определяем временной диапазон на основе выбранного периода
        if period == 'custom':
            period_start = form.cleaned_data['custom_start_date']
            period_end = form.cleaned_data['custom_end_date']
        elif period == 'year':
            period_start = timezone.now() - timezone.timedelta(days=365)
        elif period == '6_months':
            period_start = timezone.now() - timezone.timedelta(days=180)
        elif period == '3_months':
            period_start = timezone.now() - timezone.timedelta(days=90)
        elif period == '1_month':
            period_start = timezone.now() - timezone.timedelta(days=30)
        elif period == '2_weeks':
            period_start = timezone.now() - timezone.timedelta(days=14)
        elif period == '1_week':
            period_start = timezone.now() - timezone.timedelta(days=7)
        elif period == '1_day':
            period_start = timezone.now() - timezone.timedelta(days=1)
        elif period == 'all_time':
            # Устанавливаем минимальную и максимальную даты из существующих данных аналитики
            period_start = SalesAnalytics.objects.earliest('period_start').period_start
            period_end = SalesAnalytics.objects.latest('period_end').period_end

    # Устанавливаем значения по умолчанию, если они отсутствуют
    if period_start is None:
        period_start = SalesAnalytics.objects.earliest('period_start').period_start
    if period_end is None:
        period_end = SalesAnalytics.objects.latest('period_end').period_end

    # Получение данных аналитики с учетом выбранного периода
    analytics_data = SalesAnalytics.objects.filter(
        period_start__gte=period_start,
        period_end__lte=period_end,
    )

    # Фильтрация по конкретному продукту (если указан)
    if product:
        analytics_data = analytics_data.filter(product=product)

    # Суммирование общего количества заказов и общей выручки за выбранный период
    total_orders = analytics_data.aggregate(total_sales=models.Sum('total_sales'))['total_sales'] or 0
    total_revenue = analytics_data.aggregate(total_revenue=models.Sum('total_revenue'))['total_revenue'] or 0

    # Подготовка данных для построения графиков
    labels = []
    data = []

    # Группировка данных аналитики по дням для отображения на графике
    grouped_data = analytics_data.values('period_start').annotate(
        daily_sales=models.Sum('total_sales'),
        daily_revenue=models.Sum('total_revenue')
    ).order_by('period_start')

    # Формирование меток и данных для графика
    labels = [f"{item['period_start']:%d-%m-%Y} ({item['daily_sales']} шт.)" for item in grouped_data]
    data = [float(item['daily_revenue']) for item in grouped_data]

    # Определение названия графика в зависимости от выбранного продукта
    if not product:
        graph_title = "График продаж (общий)"
    else:
        graph_title = f"График продаж (букет '{product.name}')"

    # Подготовка контекста для передачи в шаблон
    context = {
        'analytics_data': analytics_data,
        'form': form,
        'labels': labels,
        'data': data,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'graph_title': graph_title,
    }
    return render(request, 'analytics/analytics_dashboard.html', context)


@login_required
@user_passes_test(lambda user: user.is_staff)
def update_analytics(request):
    """
    Обновляет данные аналитики.

    Функция вызывает обновление данных аналитики в модели `SalesAnalytics`.
    После завершения обновления выводится сообщение о результате и осуществляется перенаправление на панель аналитики.

    Аргументы:
        request (HttpRequest): Объект HTTP-запроса, содержащий данные сеанса пользователя.

    Возвращает:
        HttpResponseRedirect: Перенаправление на панель аналитики после успешного обновления.
    """
    update_analytics_data()
    messages.success(request, 'Аналитика успешно обновлена!')
    return redirect('analytics:analytics_dashboard')


@csrf_exempt
def get_analytics_data(request):
    """
    API-эндпоинт для получения аналитических данных, вызываемый ботом.

    Эндпоинт доступен только администраторам, которые идентифицируются по `telegram_id`.
    Функция проверяет права доступа, валидирует переданные параметры, а затем возвращает данные аналитики
    в формате JSON для использования в боте.

    Аргументы:
        request (HttpRequest): Объект POST-запроса с параметрами `period_start`, `period_end`, `product_id` и `telegram_id`.

    Возвращает:
        JsonResponse: JSON-ответ с данными аналитики (общее количество заказов, выручка и подробные данные по датам).
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Попытка декодирования JSON из тела запроса
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Неверный формат данных'}, status=400)

        # Извлечение параметров из JSON-запроса
        period_start = data.get('period_start')
        period_end = data.get('period_end')
        product_id = data.get('product_id')
        telegram_id = data.get('telegram_id')  # Telegram ID для идентификации пользователя

        # Проверка наличия Telegram ID
        if not telegram_id:
            return JsonResponse({'status': 'error', 'message': 'Telegram ID не предоставлен.'}, status=403)

        # Проверка существования профиля пользователя с данным Telegram ID
        try:
            profile = Profile.objects.get(telegram_id=telegram_id)
            user = profile.user
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'}, status=403)

        # Проверка прав доступа (пользователь должен быть администратором)
        if not user.is_staff:
            return JsonResponse({'status': 'error', 'message': 'Доступ запрещен. Требуются права администратора.'}, status=403)

        # Валидация формата дат
        try:
            period_start = timezone.datetime.strptime(period_start, '%Y-%m-%d')
            period_end = timezone.datetime.strptime(period_end, '%Y-%m-%d')
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат дат'}, status=400)

        # Фильтрация данных аналитики по переданным параметрам
        analytics_data = SalesAnalytics.objects.filter(
            period_start__gte=period_start,
            period_end__lte=period_end,
        )

        # Фильтрация по продукту (если указан ID продукта)
        if product_id:
            analytics_data = analytics_data.filter(product_id=product_id)

        # Суммирование общего количества заказов и общей выручки
        total_orders = analytics_data.aggregate(total_sales=models.Sum('total_sales'))['total_sales'] or 0
        total_revenue = analytics_data.aggregate(total_revenue=models.Sum('total_revenue'))['total_revenue'] or 0

        result = {
            'status': 'success',
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'data': list(analytics_data.values('period_start', 'total_sales', 'total_revenue')),
        }

        return JsonResponse(result, status=200)

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=405)
