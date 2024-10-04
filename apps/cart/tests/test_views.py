# apps/cart/tests/test_views.py

from django.contrib.auth import get_user_model  # Импорт функции для получения пользовательской модели
from django.core.files.uploadedfile import SimpleUploadedFile  # Импорт для загрузки тестовых файлов
from django.test import Client, TestCase  # Импорт тестовых классов для создания тестов и клиента
from django.urls import reverse  # Импорт для формирования URL по имени маршрута

from PIL import Image  # Импорт библиотеки для работы с изображениями
import tempfile  # Импорт временных файлов для создания тестовых изображений

from apps.cart.models import Cart, CartItem  # Импорт моделей корзины и элементов корзины
from apps.catalog.models import Product  # Импорт модели продукта

# Получение пользовательской модели для создания тестовых пользователей
User = get_user_model()


class CartViewsTest(TestCase):
    """
    Набор тестов для проверки работы представлений (views) приложения корзины.

    Тестируется добавление товаров в корзину, удаление товаров, обновление количества,
    а также корректное отображение содержимого корзины и взаимодействие с продуктами.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Инициализация тестовых данных перед запуском тестов.

        Создает тестового пользователя, фиктивное изображение и два тестовых продукта (букета),
        которые будут использоваться для проверки корректности работы представлений корзины.
        """
        # Создание тестового пользователя
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

        # Создание фиктивного изображения для использования в тестах
        cls.image = cls.create_test_image()

        # Создание тестовых продуктов с заглушкой изображения
        cls.product_1 = Product.objects.create(
            name="Розы красные",
            price=3000.0,
            description="Красные розы для любимых",
            is_available=True,
            image=cls.image,
        )
        cls.product_2 = Product.objects.create(
            name="Букет с лилиями",
            price=4500.0,
            description="Букет с ароматными лилиями",
            is_available=True,
            image=cls.image,
        )

    def setUp(self):
        """
        Настройка клиента для каждого теста.

        Логинит тестового пользователя для выполнения действий, требующих аутентификации.
        """
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_add_to_cart(self):
        """
        Тест добавления товара в корзину.

        Проверяет, что при добавлении товара в корзину создается новый элемент корзины
        и корректно увеличивается его количество.
        """
        url = reverse('cart:add_to_cart', args=[self.product_1.pk])
        response = self.client.post(url, {'quantity': 2})  # Добавление 2 единиц товара
        self.assertEqual(response.status_code, 302)  # Ожидается редирект после добавления товара

        # Проверка, что товар добавлен в корзину
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        cart_item = CartItem.objects.get(cart=cart, product=self.product_1)
        self.assertEqual(cart_item.product, self.product_1)
        self.assertEqual(cart_item.quantity, 2)

    def test_add_to_cart_from_history(self):
        """
        Тест добавления товара в корзину из истории заказов.

        Проверяет, что товар из истории заказов добавляется в корзину с указанным количеством.
        """
        url = reverse('cart:add_to_cart_from_history', args=[self.product_2.pk])
        response = self.client.post(url, {'quantity': 1})
        self.assertEqual(response.status_code, 302)  # Ожидается редирект после добавления товара

        # Проверка, что товар добавлен в корзину
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        cart_item = CartItem.objects.get(cart=cart, product=self.product_2)
        self.assertEqual(cart_item.product, self.product_2)
        self.assertEqual(cart_item.quantity, 1)

    def test_cart_detail_view(self):
        """
        Тест отображения содержимого корзины.

        Проверяет, что корзина отображает все добавленные товары и корректно отображает шаблон.
        """
        # Создаем корзину и добавляем в неё элемент
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product_1, quantity=3)

        url = reverse('cart:cart_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart_detail.html')
        self.assertContains(response, 'Ваша корзина цветов')  # Проверяем, что заголовок присутствует

    def test_update_cart_item(self):
        """
        Тест обновления количества товара в корзине.

        Проверяет, что количество конкретного товара в корзине корректно обновляется
        на указанное значение.
        """
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product_1, quantity=1)
        url = reverse('cart:update_cart_item', args=[cart_item.pk])
        response = self.client.post(url, {'quantity': 5})  # Обновляем количество товара до 5
        self.assertEqual(response.status_code, 302)  # Ожидается редирект после обновления
        cart_item.refresh_from_db()  # Обновляем данные из БД
        self.assertEqual(cart_item.quantity, 5)  # Проверяем, что количество обновилось

    def test_remove_from_cart(self):
        """
        Тест удаления товара из корзины.

        Проверяет, что товар корректно удаляется из корзины и количество элементов уменьшается.
        """
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(cart=cart, product=self.product_1, quantity=2)
        url = reverse('cart:remove_from_cart', args=[cart_item.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Ожидается редирект после удаления
        self.assertEqual(cart.items.count(), 0)  # Проверка, что корзина пуста после удаления товара

    def test_cart_detail_view_no_items(self):
        """
        Тест отображения пустой корзины.

        Проверяет, что страница корзины отображает сообщение о пустой корзине,
        если в корзине нет товаров.
        """
        url = reverse('cart:cart_detail')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ваша корзина пуста')  # Проверка, что отображается сообщение о пустой корзине

    @staticmethod
    def create_test_image():
        """
        Создание фиктивного изображения для тестов.

        Создает временное изображение 100x100 пикселей, которое используется для проверки
        добавления товаров с изображением в корзину.
        """
        image = Image.new('RGB', (100, 100), 'red')  # Создаем изображение 100x100 красного цвета
        temp_image = tempfile.NamedTemporaryFile(suffix='.jpg')  # Временный файл с расширением .jpg
        image.save(temp_image, format='JPEG')
        temp_image.seek(0)  # Возвращаем указатель в начало файла для дальнейшего использования
        return SimpleUploadedFile(temp_image.name, temp_image.read(), content_type='image/jpeg')
