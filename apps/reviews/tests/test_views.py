# apps/reviews/tests/test_views.py

from django.test import TestCase, Client  # Импорт классов для тестирования и создания тестового клиента
from django.urls import reverse  # Импорт функции reverse для генерации URL по имени маршрута
from django.contrib.auth import get_user_model  # Функция для получения пользовательской модели

from apps.catalog.models import Product  # Импорт модели продукта из приложения каталога
from apps.reviews.models import Review  # Импорт модели отзыва из текущего приложения

User = get_user_model()  # Получение пользовательской модели


class ReviewViewsTest(TestCase):
    """
    Набор тестов для проверки представлений в приложении reviews.

    Тестируемые сценарии:
    1. GET-запрос к представлению добавления отзыва.
    2. POST-запрос к представлению добавления отзыва.
    3. GET-запрос к представлению редактирования отзыва.
    4. POST-запрос к представлению редактирования отзыва.
    5. Доступ неавторизованного пользователя к добавлению отзыва.
    6. Доступ неавторизованного пользователя к редактированию отзыва.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Устанавливает начальные данные для всех тестов класса.

        Создает тестового пользователя, продукт, отзыв и тестовый клиент.
        """
        cls.user = User.objects.create_user(username='testuser', password='testpassword')  # Создание тестового пользователя
        cls.product = Product.objects.create(
            name='Тестовый букет',
            price=1000,
            description='Описание тестового букета',
            is_available=True
        )  # Создание тестового продукта
        cls.review = Review.objects.create(
            product=cls.product,
            user=cls.user,
            rating=4,
            comment='Хороший букет'
        )  # Создание тестового отзыва
        cls.client = Client()  # Создание тестового клиента

    def setUp(self):
        """
        Выполняется перед каждым тестом.

        Логинит тестового пользователя для выполнения авторизованных запросов.
        """
        self.client.login(username='testuser', password='testpassword')  # Авторизация тестового пользователя

    def test_add_review_view_get(self):
        """
        Тестирует GET-запрос к представлению добавления отзыва.

        Проверяет, что страница детали продукта отображается корректно и содержит форму добавления отзыва.
        """
        url = reverse('catalog:product_detail', args=[self.product.pk])  # Генерация URL для страницы продукта
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка успешного ответа
        self.assertTemplateUsed(response, 'catalog/product_detail.html')  # Проверка использования корректного шаблона
        self.assertContains(response, 'Добавить отзыв')  # Проверка наличия формы добавления отзыва

    def test_add_review_view_post(self):
        """
        Тестирует POST-запрос к представлению добавления отзыва.

        Проверяет, что отзыв сохраняется и происходит редирект после успешной отправки формы.
        """
        url = reverse('reviews:add_review', args=[self.product.pk])  # Генерация URL для добавления отзыва
        data = {'rating': 5, 'comment': 'Отличный букет!'}  # Данные для отправки в форму
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешного добавления
        self.assertTrue(
            Review.objects.filter(product=self.product, user=self.user, comment='Отличный букет!').exists()
        )  # Проверка сохранения отзыва в базе данных

    def test_edit_review_view_get(self):
        """
        Тестирует GET-запрос к представлению редактирования отзыва.

        Проверяет, что страница редактирования отзыва отображается корректно и содержит предзаполненную форму.
        """
        url = reverse('reviews:edit_review', args=[self.review.id])  # Генерация URL для редактирования отзыва
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка успешного ответа
        self.assertTemplateUsed(response, 'catalog/product_detail.html')  # Проверка использования корректного шаблона
        self.assertContains(response, 'Редактировать')  # Проверка наличия кнопки редактирования
        self.assertContains(response, self.review.comment)  # Проверка предзаполненных данных в форме

    def test_edit_review_view_post(self):
        """
        Тестирует POST-запрос к представлению редактирования отзыва.

        Проверяет, что отзыв обновляется и происходит редирект после успешной отправки формы.
        """
        url = reverse('reviews:edit_review', args=[self.review.id])  # Генерация URL для редактирования отзыва
        data = {'rating': 5, 'comment': 'Прекрасный букет!'}  # Новые данные для обновления отзыва
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа после успешного обновления
        self.review.refresh_from_db()  # Обновление объекта отзыва из базы данных
        self.assertEqual(self.review.rating, 5)  # Проверка обновления рейтинга
        self.assertEqual(self.review.comment, 'Прекрасный букет!')  # Проверка обновления комментария

    def test_add_review_view_unauthenticated(self):
        """
        Тестирует доступ к добавлению отзыва для неавторизованного пользователя.

        Проверяет, что происходит редирект на страницу входа при попытке доступа без авторизации.
        """
        self.client.logout()  # Выход из системы
        url = reverse('reviews:add_review', args=[self.product.pk])  # Генерация URL для добавления отзыва
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа для неавторизованного пользователя
        self.assertIn('/users/login/', response.url)  # Проверка редиректа на страницу входа

    def test_edit_review_view_unauthenticated(self):
        """
        Тестирует доступ к редактированию отзыва для неавторизованного пользователя.

        Проверяет, что происходит редирект на страницу входа при попытке доступа без авторизации.
        """
        self.client.logout()  # Выход из системы
        url = reverse('reviews:edit_review', args=[self.review.id])  # Генерация URL для редактирования отзыва
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Проверка редиректа для неавторизованного пользователя
        self.assertIn('/users/login/', response.url)  # Проверка редиректа на страницу входа
