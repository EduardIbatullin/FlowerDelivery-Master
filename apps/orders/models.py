# apps/orders/models.py

from django.db import models
from django.conf import settings  # Используем кастомную модель пользователя
from apps.catalog.models import Product  # Импортируем модель Product
from django.utils import timezone  # Импортируем timezone для текущей даты и времени


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=50, verbose_name='Статус заказа')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')

    # Новые поля
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    products = models.ManyToManyField(Product, verbose_name='Товары', related_name='orders')

    def __str__(self):
        return f"Order {self.id} by {self.user}"
