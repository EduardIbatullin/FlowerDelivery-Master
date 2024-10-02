# apps/cart/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.cart.models import Cart, CartItem

User = get_user_model()


class CartModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание пользователя
        cls.user = User.objects.create_user(username='testuser', password='password')

        # Создание продуктов
        cls.product_1 = Product.objects.create(name="Розы", price=3000.0, description="Красные розы")
        cls.product_2 = Product.objects.create(name="Лилии", price=4500.0, description="Белые лилии")

        # Создание корзины для пользователя
        cls.cart = Cart.objects.create(user=cls.user)

    def test_cart_creation(self):
        """Тест создания корзины для пользователя."""
        self.assertEqual(str(self.cart), f"Корзина пользователя {self.user.username}")

    def test_add_product_to_cart(self):
        """Тест добавления продукта в корзину."""
        self.cart.add_product(self.product_1, 2)
        cart_items = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.first().product, self.product_1)
        self.assertEqual(cart_items.first().quantity, 2)

    def test_cart_total_price(self):
        """Тест вычисления общей стоимости корзины."""
        # Добавляем два продукта в корзину
        self.cart.add_product(self.product_1, 2)  # 2 * 3000 = 6000
        self.cart.add_product(self.product_2, 1)  # 1 * 4500 = 4500

        self.assertEqual(self.cart.total_price(), 10500.0)  # Общая стоимость = 6000 + 4500

    def test_cart_item_total_price(self):
        """Тест вычисления стоимости CartItem."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product_1, quantity=3)
        self.assertEqual(cart_item.total_price(), 9000.0)  # 3 * 3000 = 9000

    def test_remove_product_from_cart(self):
        """Тест удаления продукта из корзины."""
        self.cart.add_product(self.product_1, 2)
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product_1)
        cart_item.delete()
        self.assertEqual(self.cart.items.count(), 0)
