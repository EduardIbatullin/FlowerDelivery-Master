# apps/orders/tests/test_views.py

from django.test import TestCase, Client  # Импортируем базовые классы для тестов и клиента для запросов
from django.urls import reverse  # Импортируем функцию для получения URL по имени маршрута
from django.contrib.auth import get_user_model  # Импорт функции для получения модели пользователя
from django.core.files.uploadedfile import SimpleUploadedFile  # Импортируем класс для работы с загруженными файлами

from apps.orders.models import Order, OrderItem  # Импортируем модели заказа и элемента заказа
from apps.catalog.models import Product  # Импортируем модель продукта для тестирования
from apps.cart.models import Cart, CartItem  # Импортируем модели корзины и элементов корзины


User = get_user_model()  # Получаем кастомную модель пользователя


class OrdersViewsTest(TestCase):
    """
    Набор тестов для проверки представлений приложения управления заказами (orders).

    Включает тесты на проверку доступа к списку заказов, истории изменения статусов, деталей заказа,
    а также изменение статуса заказа для администратора. Дополнительно проверяется доступ для обычных пользователей.
    """

    def setUp(self):
        """
        Метод инициализации данных перед запуском тестов.

        Создает тестового пользователя, аутентифицирует клиента, создает корзину и заглушку для изображения.
        """
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()  # Инициализация клиента для запросов
        self.client.login(username='testuser', password='testpassword')  # Аутентификация клиента
        self.cart = Cart.objects.create(user=self.user)  # Создаем корзину для тестового пользователя

        # Создание заглушки изображения
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        # Создание тестового продукта с изображением
        self.product = Product.objects.create(
            name='Тестовый букет',
            price=500,
            description='Описание тестового букета',
            is_available=True,
            image=self.image
        )
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)

    def test_order_create_view_get(self):
        """
        Тест GET-запроса к странице создания заказа.

        Проверяет, что страница создания заказа возвращает статус 200.
        """
        response = self.client.get(reverse('orders:order_create'))
        self.assertEqual(response.status_code, 200)

    def test_order_summary_view_get(self):
        """
        Тест GET-запроса к странице подтверждения заказа.

        Проверяет, что страница подтверждения заказа возвращает статус 200.
        """
        # Подготовка сессии с данными заказа
        session = self.client.session
        session['order_data'] = {
            'delivery_address': 'Тестовый адрес',
            'contact_phone': '1234567890',
            'delivery_date': '2024-10-10',
            'delivery_time': '10:00',
            'additional_info': 'Комментарий',
        }
        session.save()

        response = self.client.get(reverse('orders:order_summary'))
        self.assertEqual(response.status_code, 200)

    def test_order_summary_post_confirm_order(self):
        """
        Тест POST-запроса подтверждения заказа.

        Проверяет, что подтверждение заказа возвращает статус 302 (редирект).
        """
        # Подготовка сессии с данными заказа
        session = self.client.session
        session['order_data'] = {
            'delivery_address': 'Тестовый адрес',
            'contact_phone': '1234567890',
            'delivery_date': '2024-10-10',
            'delivery_time': '10:00',
            'additional_info': 'Комментарий',
        }
        session.save()

        response = self.client.post(reverse('orders:order_summary'), {'confirm_order': True})
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после подтверждения заказа

    def test_order_success_view_get(self):
        """
        Тест GET-запроса к странице успешного создания заказа.

        Проверяет, что страница успешного завершения заказа возвращает статус 200.
        """
        response = self.client.get(reverse('orders:order_success'))
        self.assertEqual(response.status_code, 200)

    def test_delete_item_view_post(self):
        """
        Тест POST-запроса на удаление элемента корзины.

        Проверяет, что элемент корзины удаляется и возвращается статус 302 (редирект).
        """
        # Проверяем, что элемент корзины существует перед удалением
        cart_item_id = self.cart_item.id  # Сохраняем идентификатор элемента корзины

        # Убедимся, что элемент корзины присутствует в корзине пользователя
        self.assertTrue(CartItem.objects.filter(cart=self.cart, pk=cart_item_id).exists())

        # Отправляем POST-запрос на удаление элемента корзины
        response = self.client.post(reverse('orders:delete_item', args=[cart_item_id]))
        self.assertEqual(response.status_code, 302)  # Предполагаем, что происходит редирект после удаления

        # Проверяем, что элемент корзины больше не существует после удаления
        self.assertFalse(CartItem.objects.filter(cart=self.cart, pk=cart_item_id).exists())

    def test_order_history_view_get(self):
        """
        Тест GET-запроса к странице истории заказов.

        Проверяет, что страница истории заказов возвращает статус 200.
        """
        response = self.client.get(reverse('orders:order_history'))
        self.assertEqual(response.status_code, 200)

    def test_update_cart_view_post(self):
        """
        Тест POST-запроса на обновление корзины.

        Проверяет, что количество товара обновляется и возвращается статус 302 (редирект).
        """
        response = self.client.post(reverse('orders:update_cart'), {
            f'quantity_{self.product.id}': 2  # Используем корректный идентификатор товара
        })
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после обновления

        # Проверка, что количество товара обновилось
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 2)

    def test_update_order_item_view_post(self):
        """
        Тест POST-запроса на обновление элемента заказа.

        Проверяет, что количество товара в заказе обновляется и возвращается статус 302 (редирект).
        """
        order = Order.objects.create(user=self.user, total_price=1000)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1,
                                              price_at_purchase=self.product.price)

        response = self.client.post(reverse('orders:update_order_item', args=[order_item.id]), {
            'quantity': 5  # Обновляем количество товара в заказе
        })
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после обновления

        # Обновляем объект из базы данных и проверяем количество
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 5)  # Проверка, что количество товара в заказе обновилось
