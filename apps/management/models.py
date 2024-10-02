# apps/management/models.py

from django.db import models
from apps.orders.models import Order
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, related_name='status_history', on_delete=models.CASCADE, verbose_name="Заказ")
    previous_status = models.CharField(max_length=50, verbose_name="Предыдущий статус")
    new_status = models.CharField(max_length=50, verbose_name="Новый статус")
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Изменено пользователем")
    changed_at = models.DateTimeField(default=timezone.now, verbose_name="Дата изменения")

    def __str__(self):
        return f"Заказ #{self.order.id}: {self.previous_status} → {self.new_status} (Изменено: {self.changed_by})"
