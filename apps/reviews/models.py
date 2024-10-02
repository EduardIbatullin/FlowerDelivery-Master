# apps/reviews/models.py

from django.db import models
from apps.catalog.models import Product
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="Букет")
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.PositiveSmallIntegerField(verbose_name="Оценка", choices=[(i, i) for i in range(1, 6)], default=5)
    comment = models.TextField(verbose_name="Текст отзыва", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    def __str__(self):
        return f"Отзыв на {self.product.name} от {self.user.username}: {self.rating} звёзд"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
