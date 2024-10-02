# apps/orders/models.py

from django.db import models
from django.conf import settings
from apps.catalog.models import Product
from django.utils import timezone


class Order(models.Model):
    STATUS_CHOICES = [
        ('В ожидании', 'В ожидании'),
        ('В обработке', 'В обработке'),
        ('В дороге', 'В дороге'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='В ожидании', verbose_name='Статус заказа')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Общая стоимость')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    contact_phone = models.CharField(max_length=20, default='', verbose_name='Контактный телефон')
    delivery_date = models.DateField(verbose_name='Дата доставки', default=timezone.now)
    delivery_time = models.TimeField(verbose_name='Время доставки', default=timezone.now)
    additional_info = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')
    email_notifications = models.BooleanField(default=False, verbose_name='Уведомления по email')
    telegram_notifications = models.BooleanField(default=False, verbose_name='Уведомления по Telegram')
    complete = models.BooleanField(default=False, verbose_name="Заказ завершен")

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def get_total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    """
    Промежуточная модель для хранения информации о каждом товаре в заказе
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена при покупке')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} для заказа {self.order.id}"

    @property
    def total_price(self):
        return self.quantity * self.price_at_purchase
