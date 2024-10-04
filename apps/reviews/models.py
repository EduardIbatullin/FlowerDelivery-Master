# app/apps/reviews/models.py

from django.db import models  # Импорт базовых классов моделей Django
from django.contrib.auth import get_user_model  # Функция для получения пользовательской модели

from apps.catalog.models import Product  # Импорт модели Product из приложения каталога

User = get_user_model()  # Получение пользовательской модели, используемой в проекте


class Review(models.Model):
    """
    Модель, представляющая отзыв пользователя о продукте.

    Содержит информацию о продукте, пользователе, оценке, комментарии и дате создания отзыва.

    Атрибуты:
        product (ForeignKey): Ссылка на продукт, к которому относится отзыв.
        user (ForeignKey): Ссылка на пользователя, оставившего отзыв.
        rating (PositiveSmallIntegerField): Оценка продукта по шкале от 1 до 5.
        comment (TextField): Текстовый комментарий пользователя.
        created_at (DateTimeField): Дата и время создания отзыва.
    """

    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name="Букет"
    )  # Связь с продуктом, к которому относится отзыв

    user = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )  # Связь с пользователем, оставившим отзыв

    rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        default=5,
        verbose_name="Оценка"
    )  # Оценка продукта от 1 до 5

    comment = models.TextField(
        blank=True,
        verbose_name="Текст отзыва"
    )  # Текстовый комментарий к отзыву

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата отзыва"
    )  # Дата и время создания отзыва

    def __str__(self):
        """
        Возвращает строковое представление отзыва.

        Возвращает:
            str: Строка формата "Отзыв на <название продукта> от <имя пользователя>: <оценка> звёзд".
        """
        return f"Отзыв на {self.product.name} от {self.user.username}: {self.rating} звёзд"

    class Meta:
        """
        Метаданные модели Review.

        Атрибуты:
            verbose_name (str): Название модели в единственном числе.
            verbose_name_plural (str): Название модели во множественном числе.
            ordering (list): Порядок сортировки отзывов по умолчанию.
        """
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']
