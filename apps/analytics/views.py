from django.shortcuts import render
from django.db.models import Sum
from apps.orders.models import Order


def sales_report_view(request):
    orders = Order.objects.all()
    total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    return render(request, 'analytics/sales_report.html', {'orders': orders, 'total_sales': total_sales})


def profit_analysis_view(request):
    # Пример анализа прибыли (можно добавить свои расчеты)
    orders = Order.objects.all()
    total_profit = sum(order.total_price for order in orders)  # Простая сумма всех заказов как пример
    return render(request, 'analytics/profit_analysis.html', {'total_profit': total_profit})
