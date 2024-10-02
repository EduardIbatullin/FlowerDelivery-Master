# apps/reviews/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.reviews.models import Review

User = get_user_model()


class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создание тестового пользователя и продукта
        cls.user = User.objects.create_user(username='testuser', password='password')
        cls.product = Product.objects.create(name="Тестовый букет", price=5000.0,
                                             description="Описание тестового букета")

    def test_create_review(self):
        """Проверка создания отзыва."""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Отличный букет!"
        )
        self.assertEqual(review.product, self.product)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Отличный букет!")
        self.assertTrue(review.created_at)

    def test_review_str(self):
        """Проверка строкового представления модели Review."""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Отличный букет!"
        )
        expected_str = f"Отзыв на {self.product.name} от {self.user.username}: {review.rating} звёзд"
        self.assertEqual(str(review), expected_str)

    def test_default_rating_value(self):
        """Проверка значения по умолчанию для поля rating."""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            comment="Букет без оценки"
        )
        self.assertEqual(review.rating, 5)

    def test_delete_product_cascade(self):
        """Проверка каскадного удаления отзыва при удалении продукта."""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Отличный букет!"
        )
        product_id = self.product.id  # Сохраняем идентификатор продукта
        self.product.delete()  # Удаляем продукт

        # Проверяем, что отзыв удален после удаления продукта
        reviews_count = Review.objects.filter(product_id=product_id).count()
        self.assertEqual(reviews_count, 0)

    def test_delete_user_cascade(self):
        """Проверка каскадного удаления отзыва при удалении пользователя."""
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Отличный букет!"
        )
        user_id = self.user.id  # Сохраняем идентификатор пользователя
        self.user.delete()  # Удаляем пользователя

        # Проверяем, что отзыв удален после удаления пользователя
        reviews_count = Review.objects.filter(user_id=user_id).count()
        self.assertEqual(reviews_count, 0)
