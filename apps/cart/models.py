# apps/cart/models.py

from django.conf import settings
from django.db import models
from apps.catalog.models import Product


class Cart(models.Model):
    """
    Модель корзины пользователя. Связана с конкретным пользователем.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_product(self, product, quantity=1):
        """
        Метод для добавления продукта в корзину или обновления количества, если продукт уже в корзине.
        """
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return cart_item

    def total_price(self):
        """
        Подсчет общей стоимости всех товаров в корзине.
        """
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    """
    Модель элемента корзины, связана с конкретной корзиной и продуктом.
    """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """
        Подсчет общей стоимости данного элемента корзины.
        """
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
