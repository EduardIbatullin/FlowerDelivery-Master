# apps/reviews/tests/test_models.py

from django.test import TestCase  # Импорт базового класса для создания тестов с базой данных
from django.contrib.auth import get_user_model  # Импорт функции для получения пользовательской модели

from apps.catalog.models import Product  # Импорт модели Product для создания тестовых данных
from apps.reviews.models import Review  # Импорт модели Review для тестирования ее функциональности

User = get_user_model()  # Получение текущей пользовательской модели


class ReviewModelTest(TestCase):
    """
    Набор тестов для проверки модели `Review` в приложении reviews.

    Тестируемые сценарии:
    1. Создание отзыва и проверка его полей.
    2. Проверка строкового представления (`__str__`) модели Review.
    3. Проверка значения по умолчанию для поля `rating`.
    4. Проверка каскадного удаления отзывов при удалении продукта.
    5. Проверка каскадного удаления отзывов при удалении пользователя.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Устанавливает начальные данные для всех тестов класса.

        Создает тестового пользователя и тестовый продукт, которые будут использоваться в тестах.
        """
        # Создание тестового пользователя
        cls.user = User.objects.create_user(username='testuser', password='password')
        # Создание тестового продукта
        cls.product = Product.objects.create(
            name="Тестовый букет",
            price=5000.0,
            description="Описание тестового букета"
        )

    def test_create_review(self):
        """
        Проверяет корректность создания отзыва.

        Убеждается, что отзыв сохраняется с правильными значениями полей и устанавливается поле `created_at`.
        """
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
        self.assertIsNotNone(review.created_at)

    def test_review_str(self):
        """
        Проверяет строковое представление модели `Review`.

        Убеждается, что метод `__str__` возвращает корректную строку с информацией об отзыве.
        """
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            rating=4,
            comment="Отличный букет!"
        )
        expected_str = f"Отзыв на {self.product.name} от {self.user.username}: {review.rating} звёзд"
        self.assertEqual(str(review), expected_str)

    def test_default_rating_value(self):
        """
        Проверяет значение по умолчанию для поля `rating`.

        Убеждается, что если оценка не указана, то устанавливается значение по умолчанию равное 5.
        """
        review = Review.objects.create(
            product=self.product,
            user=self.user,
            comment="Букет без оценки"
        )
        self.assertEqual(review.rating, 5)

    def test_delete_product_cascade(self):
        """
        Проверяет каскадное удаление отзывов при удалении продукта.

        Убеждается, что при удалении продукта все связанные с ним отзывы также удаляются.
        """
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
        """
        Проверяет каскадное удаление отзывов при удалении пользователя.

        Убеждается, что при удалении пользователя все его отзывы также удаляются.
        """
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
