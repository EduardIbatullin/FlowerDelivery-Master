# apps/cart/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.cart.models import Cart, CartItem
import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class CartViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создаем тестового пользователя
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создаем фиктивное изображение
        cls.image = cls.create_test_image()

        # Создаем продукты для тестирования
        cls.product_1 = Product.objects.create(
            name="Розы красные",
            price=3000.0,
            description="Красные розы для любимых",
            is_available=True,
            image=cls.image,  # Добавляем заглушку изображения
        )
        cls.product_2 = Product.objects.create(
            name="Букет с лилиями",
            price=4500.0,
            description="Букет с ароматными лилиями",
            is_available=True,
            image=cls.image,  # Добавляем заглушку изображения
        )

    def setUp(self):
        # Инициализация клиента для каждого теста
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')  # Логинимся для доступа к представлениям

    def test_add_to_cart(self):
        """Тест добавления товара в корзину."""
        url = reverse('cart:add_to_cart', args=[self.product_1.pk])
        response = self.client.post(url, {'quantity': 2})
        self.assertEqual(response.status_code, 302)  # Должен произойти редирект
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        cart_item = CartItem.objects.get(cart=cart, product=self.product_1)
        self.assertEqual(cart_item.product, self.product_1)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_from_history(self):
        """Тест добавления товара в корзину из истории заказов."""
        url = reverse('cart:add_to_cart_from_history', args=[self.product_2.pk])
        response = self.client.post(url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)  # Должен произойти редирект на историю заказов
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        cart_item = CartItem.objects.get(cart=cart, product=self.product_2)
        self.assertEqual(cart_item.product, self.product_2)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_detail_view(self):
        """Тест отображения корзины пользователя."""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product_1, quantity=3)
        url = reverse('cart:cart_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
        self.assertContains(response, 'Ваша корзина цветов')

    def test_update_cart_item(self):
        """Тест обновления количества товара в корзине."""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product_1, quantity=1)
        url = reverse('cart:update_cart_item', args=[cart_item.pk])
        response = self.client.post(url, {'quantity': 5})
        self.assertEqual(response.status_code, 302)  # Должен произойти редирект на страницу корзины
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)

    def test_remove_from_cart(self):
        """Тест удаления товара из корзины."""
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product_1, quantity=2)
        url = reverse('cart:remove_from_cart', args=[cart_item.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Должен произойти редирект на страницу корзины
        self.assertEqual(cart.items.count(), 0)  # Проверяем, что товар удален из корзины

    def test_cart_detail_view_no_items(self):
        """Тест отображения пустой корзины."""
        url = reverse('cart:cart_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ваша корзина пуста')

    @staticmethod
    def create_test_image():
        """Создание фиктивного изображения для тестов."""
        # Создаем временное изображение 100x100
        image = Image.new('RGB', (100, 100), 'red')
        temp_image = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(temp_image, format='JPEG')
        temp_image.seek(0)  # Возвращаем указатель в начало файла
        return SimpleUploadedFile(temp_image.name, temp_image.read(), content_type='image/jpeg')
