# apps/reviews/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.reviews.models import Review

User = get_user_model()


class ReviewViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестового пользователя и продукта
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        cls.product = Product.objects.create(
            name='Тестовый букет',
            price=1000,
            description='Описание тестового букета',
            is_available=True
        )
        # Создаем тестовый отзыв
        cls.review = Review.objects.create(
            product=cls.product,
            user=cls.user,
            rating=4,
            comment='Хороший букет'
        )
        # Создаем клиент для тестов
        cls.client = Client()

    def setUp(self):
        # Логинимся перед каждым тестом
        self.client.login(username='testuser', password='testpassword')

    def test_add_review_view_get(self):
        """Тест GET-запроса к представлению добавления отзыва."""
        url = reverse('catalog:product_detail', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка на успешный статус
        self.assertTemplateUsed(response, 'catalog/product_detail.html')  # Проверка на использование корректного шаблона
        self.assertContains(response, 'Добавить отзыв')  # Проверка наличия формы добавления отзыва на странице

    def test_add_review_view_post(self):
        """Тест POST-запроса к представлению добавления отзыва."""
        url = reverse('reviews:add_review', args=[self.product.pk])
        data = {'rating': 5, 'comment': 'Отличный букет!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после успешного добавления
        self.assertTrue(Review.objects.filter(product=self.product, user=self.user, comment='Отличный букет!').exists())

    def test_edit_review_view_get(self):
        """Тест GET-запроса к представлению редактирования отзыва."""
        url = reverse('reviews:edit_review', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Проверка на успешный статус
        self.assertTemplateUsed(response, 'catalog/product_detail.html')  # Проверка на использование корректного шаблона
        self.assertContains(response, 'Редактировать')  # Проверка наличия кнопки редактирования
        # Проверяем, что форма редактирования предзаполнена данными отзыва
        self.assertContains(response, self.review.comment)

    def test_edit_review_view_post(self):
        """Тест POST-запроса к представлению редактирования отзыва."""
        url = reverse('reviews:edit_review', args=[self.review.id])
        data = {'rating': 5, 'comment': 'Прекрасный букет!'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Проверка на редирект после успешного обновления
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Прекрасный букет!')

    def test_add_review_view_unauthenticated(self):
        """Тест доступа к добавлению отзыва неавторизованного пользователя."""
        self.client.logout()
        url = reverse('reviews:add_review', args=[self.product.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Должен произойти редирект на страницу входа

    def test_edit_review_view_unauthenticated(self):
        """Тест доступа к редактированию отзыва неавторизованного пользователя."""
        self.client.logout()
        url = reverse('reviews:edit_review', args=[self.review.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Должен произойти редирект на страницу входа
