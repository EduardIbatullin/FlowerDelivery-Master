# apps/analytics/models.py

from django.db import models
from apps.catalog.models import Product


class SalesAnalytics(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_analytics', verbose_name='Букет')
    total_sales = models.IntegerField(default=0, verbose_name='Общее количество продаж')
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Общая выручка')
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                              verbose_name='Средняя стоимость заказа')
    period_start = models.DateField(verbose_name='Начало периода')
    period_end = models.DateField(verbose_name='Конец периода')

    def __str__(self):
        return f"Аналитика продаж: {self.product.name} ({self.period_start} - {self.period_end})"

    class Meta:
        verbose_name = "Аналитика продаж"
        verbose_name_plural = "Аналитика продаж"
