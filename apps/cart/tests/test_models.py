# apps/cart/tests/test_models.py

from django.contrib.auth import get_user_model  # Импорт пользовательской модели для работы с пользователями в тестах
from django.test import TestCase  # Импорт тестового класса TestCase для написания тестов

from apps.cart.models import Cart, CartItem  # Импорт моделей корзины и элементов корзины для тестирования их функционала
from apps.catalog.models import Product  # Импорт модели Product для создания тестовых продуктов в корзине

# Получение пользовательской модели
User = get_user_model()


class CartModelTest(TestCase):
    """
    Набор тестов для проверки моделей корзины (`Cart`) и элементов корзины (`CartItem`).

    Тестируется создание корзины, добавление продуктов в корзину, вычисление общей стоимости,
    а также удаление элементов из корзины.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Инициализация тестовых данных перед запуском тестов.

        Создает тестового пользователя, тестовые продукты (букеты) и корзину для пользователя.
        Эти данные используются для тестирования различных методов и функционала корзины.
        """
        # Создание тестового пользователя
        cls.user = User.objects.create_user(username='testuser', password='password')

        # Создание тестовых продуктов (букетов)
        cls.product_1 = Product.objects.create(name="Розы", price=3000.0, description="Красные розы")
        cls.product_2 = Product.objects.create(name="Лилии", price=4500.0, description="Белые лилии")

        # Создание тестовой корзины для пользователя
        cls.cart = Cart.objects.create(user=cls.user)

    def test_cart_creation(self):
        """
        Тест создания корзины для пользователя.

        Проверяет корректность создания корзины и отображения её строкового представления.
        """
        self.assertEqual(str(self.cart), f"Корзина пользователя {self.user.username}")

    def test_add_product_to_cart(self):
        """
        Тест добавления продукта в корзину.

        Проверяет, что продукт корректно добавляется в корзину с заданным количеством.
        """
        self.cart.add_product(self.product_1, 2)  # Добавление 2 единиц продукта 1
        cart_items = CartItem.objects.filter(cart=self.cart)

        # Проверка количества элементов в корзине
        self.assertEqual(cart_items.count(), 1)
        self.assertEqual(cart_items.first().product, self.product_1)  # Проверка, что добавлен правильный продукт
        self.assertEqual(cart_items.first().quantity, 2)  # Проверка правильного количества

    def test_cart_total_price(self):
        """
        Тест вычисления общей стоимости корзины.

        Проверяет корректность подсчета общей стоимости всех товаров в корзине.
        """
        # Добавляем два продукта в корзину
        self.cart.add_product(self.product_1, 2)  # 2 * 3000 = 6000
        self.cart.add_product(self.product_2, 1)  # 1 * 4500 = 4500

        # Общая стоимость должна быть 6000 + 4500 = 10500
        self.assertEqual(self.cart.total_price(), 10500.0)

    def test_cart_item_total_price(self):
        """
        Тест вычисления стоимости конкретного элемента корзины (`CartItem`).

        Проверяет, что стоимость элемента рассчитывается правильно в зависимости от количества.
        """
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product_1, quantity=3)  # 3 * 3000
        self.assertEqual(cart_item.total_price(), 9000.0)  # 3 * 3000 = 9000

    def test_remove_product_from_cart(self):
        """
        Тест удаления продукта из корзины.

        Проверяет, что продукт корректно удаляется из корзины и элементы корзины обновляются.
        """
        self.cart.add_product(self.product_1, 2)  # Добавление 2 единиц продукта 1
        cart_item = CartItem.objects.get(cart=self.cart, product=self.product_1)  # Получение элемента корзины
        cart_item.delete()  # Удаление элемента из корзины

        # Проверка, что корзина теперь пуста
        self.assertEqual(self.cart.items.count(), 0)
