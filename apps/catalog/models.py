# apps/catalog/models.py

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True, null=True)
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        return self.name

    def average_rating(self):
        reviews = self.reviews.all()  # Получаем все отзывы, связанные с данным продуктом
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return None  # Возвращаем None, если отзывов нет

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
