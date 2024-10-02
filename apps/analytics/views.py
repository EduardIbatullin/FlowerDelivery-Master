# apps/analytics/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import JsonResponse
from .models import SalesAnalytics
from .forms import AnalyticsFilterForm
from .utils import update_analytics_data
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
import json
from apps.users.models import Profile

User = get_user_model()


@login_required
@user_passes_test(lambda user: user.is_staff)
def analytics_dashboard(request):
    """
    Отображение аналитической панели.
    """
    form = AnalyticsFilterForm(request.GET or None)

    # Параметры фильтрации по умолчанию (период: 1 месяц)
    period_start = None
    period_end = None
    product = None

    # Обработка данных из формы
    if form.is_valid():
        period = form.cleaned_data['period']
        product = form.cleaned_data['product']

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
            # Устанавливаем минимальную и максимальную даты из существующих данных
            period_start = SalesAnalytics.objects.earliest('period_start').period_start
            period_end = SalesAnalytics.objects.latest('period_end').period_end

    # Устанавливаем значения по умолчанию, если они отсутствуют
    if period_start is None:
        period_start = SalesAnalytics.objects.earliest('period_start').period_start
    if period_end is None:
        period_end = SalesAnalytics.objects.latest('period_end').period_end

    # Получение данных из модели SalesAnalytics с учетом фильтрации
    analytics_data = SalesAnalytics.objects.filter(
        period_start__gte=period_start,
        period_end__lte=period_end,
    )

    if product:
        analytics_data = analytics_data.filter(product=product)

    # Суммирование общего количества заказов и общей выручки
    total_orders = analytics_data.aggregate(total_sales=models.Sum('total_sales'))['total_sales'] or 0
    total_revenue = analytics_data.aggregate(total_revenue=models.Sum('total_revenue'))['total_revenue'] or 0

    # Подготовка данных для графиков
    labels = []
    data = []

    # Если конкретный букет не выбран, отображаем общие данные по дням
    if not product:
        # Группировка по дате и расчет общего дохода за каждый день
        grouped_data = analytics_data.values('period_start').annotate(
            daily_sales=models.Sum('total_sales'),
            daily_revenue=models.Sum('total_revenue')
        ).order_by('period_start')

        labels = [f"{item['period_start']:%d-%m-%Y} ({item['daily_sales']} шт.)" for item in grouped_data]
        data = [float(item['daily_revenue']) for item in grouped_data]
        graph_title = "График продаж (общий)"
    else:
        # Если выбран конкретный букет, отображаем доход и количество продаж за каждый день
        grouped_data = analytics_data.values('period_start').annotate(
            daily_sales=models.Sum('total_sales'),
            daily_revenue=models.Sum('total_revenue')
        ).order_by('period_start')

        labels = [f"{item['period_start']:%d-%m-%Y} ({item['daily_sales']} шт.)" for item in grouped_data]
        data = [float(item['daily_revenue']) for item in grouped_data]
        graph_title = f"График продаж (букет '{product.name}')"

    # Формирование контекста для передачи в шаблон
    context = {
        'analytics_data': analytics_data,
        'form': form,
        'labels': labels,
        'data': data,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'graph_title': graph_title,  # Передаем название графика в шаблон
    }
    return render(request, 'analytics/analytics_dashboard.html', context)


@login_required
@user_passes_test(lambda user: user.is_staff)
def update_analytics(request):
    """
    Обновление аналитических данных.
    """
    update_analytics_data()
    messages.success(request, 'Аналитика успешно обновлена!')
    return redirect('analytics:analytics_dashboard')


@csrf_exempt
def get_analytics_data(request):
    """
    API-эндпоинт для получения аналитических данных, вызываемый ботом.
    Доступен только администраторам, идентифицируемым по telegram_id.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Неверный формат данных'}, status=400)

        period_start = data.get('period_start')
        period_end = data.get('period_end')
        product_id = data.get('product_id')
        telegram_id = data.get('telegram_id')  # Получаем telegram_id из запроса

        if not telegram_id:
            return JsonResponse({'status': 'error', 'message': 'Telegram ID не предоставлен.'}, status=403)

        try:
            # Попробуем получить профиль пользователя по telegram_id
            profile = Profile.objects.get(telegram_id=telegram_id)
            user = profile.user
        except Profile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'}, status=403)

        if not user.is_staff:
            return JsonResponse({'status': 'error', 'message': 'Доступ запрещен. Требуются права администратора.'}, status=403)

        try:
            period_start = timezone.datetime.strptime(period_start, '%Y-%m-%d')
            period_end = timezone.datetime.strptime(period_end, '%Y-%m-%d')
        except (TypeError, ValueError):
            return JsonResponse({'status': 'error', 'message': 'Некорректный формат дат'}, status=400)

        analytics_data = SalesAnalytics.objects.filter(
            period_start__gte=period_start,
            period_end__lte=period_end,
        )

        if product_id:
            analytics_data = analytics_data.filter(product_id=product_id)

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
