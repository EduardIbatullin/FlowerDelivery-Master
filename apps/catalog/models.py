# apps/catalog/models.py

from django.db import models  # Импортируем модули Django для работы с моделями


class Product(models.Model):
    """
    Модель для представления продукта в каталоге магазина.

    Содержит основные поля, такие как название, цена, описание, изображение и статус наличия.
    Модель связана с отзывами, которые могут оставлять пользователи, и позволяет
    вычислять средний рейтинг продукта на основе отзывов.

    Атрибуты:
        name (str): Название продукта (букета).
        price (Decimal): Цена продукта в формате десятичного числа.
        description (str): Описание продукта, необязательное для заполнения.
        image (ImageField): Изображение продукта, загружаемое в папку `products/`.
        is_available (bool): Флаг доступности продукта для заказа.
        created_at (datetime): Дата и время создания записи о продукте.
    """
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(upload_to='products/', verbose_name="Изображение", blank=True, null=True)
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    def __str__(self):
        """
        Возвращает строковое представление продукта.

        Возвращает:
            str: Название продукта.
        """
        return self.name

    def average_rating(self):
        """
        Рассчитывает средний рейтинг продукта на основе связанных отзывов.

        Проходит по всем отзывам, связанным с данным продуктом, и вычисляет среднее значение поля `rating`.
        Если отзывов нет, возвращает `None`.

        Возвращает:
            float или None: Средний рейтинг продукта или None, если отзывов нет.
        """
        reviews = self.reviews.all()  # Получаем все отзывы, связанные с данным продуктом
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']  # Рассчитываем средний рейтинг
        return None  # Возвращаем None, если отзывов нет

    class Meta:
        """
        Дополнительные настройки модели.

        Определяет название модели и множественное название на русском языке,
        которые будут отображаться в административной панели.
        """
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
