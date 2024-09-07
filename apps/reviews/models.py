# apps/reviews/models.py

from django.db import models
from django.conf import settings  # Используем кастомную модель пользователя
from apps.catalog.models import Product  # Импортируем модель Product


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='reviews')
    rating = models.PositiveIntegerField(default=1, verbose_name='Рейтинг')
    comment = models.TextField(verbose_name='Комментарий')  # Добавляем недостающее поле 'comment'
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Review by {self.user} for {self.product}"
