# apps/cart/models.py

from django.conf import settings  # Импорт настроек проекта для работы с моделью пользователя
from django.db import models  # Импорт модуля для создания моделей Django

from apps.catalog.models import Product  # Импорт модели Product для связи с корзиной


class Cart(models.Model):
    """
    Модель корзины, связанная с пользователем.

    Хранит информацию о корзине конкретного пользователя и предоставляет методы для управления содержимым корзины,
    включая добавление продуктов и подсчет общей стоимости всех товаров.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def add_product(self, product, quantity=1):
        """
        Добавляет продукт в корзину или увеличивает его количество, если продукт уже существует в корзине.

        Если продукт уже находится в корзине, его количество увеличивается на указанное значение.
        Если продукт добавляется впервые, создается новый элемент корзины с указанным количеством.

        Аргументы:
            - product (Product): Продукт, который добавляется в корзину.
            - quantity (int): Количество добавляемого продукта (по умолчанию 1).

        Возвращает:
            - CartItem: Объект элемента корзины с обновленным количеством.
        """
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity  # Увеличение количества, если продукт уже в корзине
        else:
            cart_item.quantity = quantity  # Установка количества для нового продукта
        cart_item.save()
        return cart_item

    def total_price(self):
        """
        Рассчитывает общую стоимость всех товаров в корзине.

        Перебирает все элементы корзины и суммирует их стоимость, умножая количество каждого товара на его цену.

        Возвращает:
            - float: Общая стоимость всех товаров в корзине.
        """
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        """
        Строковое представление корзины.

        Возвращает строку, содержащую имя пользователя, который владеет корзиной.

        Возвращает:
            - str: Строка с именем пользователя.
        """
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    """
    Модель элемента корзины, связанная с корзиной и продуктом.

    Хранит информацию о количестве продукта в корзине и предоставляет метод для расчета
    общей стоимости данного элемента.
    """

    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def total_price(self):
        """
        Рассчитывает общую стоимость данного элемента корзины.

        Умножает количество продукта на его цену и возвращает итоговую стоимость.

        Возвращает:
            - float: Общая стоимость элемента корзины.
        """
        return self.quantity * self.product.price

    def __str__(self):
        """
        Строковое представление элемента корзины.

        Возвращает строку, содержащую информацию о продукте и его количестве.

        Возвращает:
            - str: Строка с названием продукта и его количеством.
        """
        return f"{self.product.name} - {self.quantity}"
