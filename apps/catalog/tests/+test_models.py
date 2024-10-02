# apps/catalog/tests/test_models.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.catalog.models import Product
from apps.reviews.models import Review

User = get_user_model()


class ProductModelTest(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Создание тестового продукта
        self.product = Product.objects.create(
            name="Тестовый букет",
            price=1000.00,
            description="Тестовое описание букета",
            is_available=True,
        )

    def test_product_creation(self):
        """Проверка создания продукта и его полей."""
        product = Product.objects.get(name="Тестовый букет")
        self.assertEqual(product.name, "Тестовый букет")
        self.assertEqual(product.price, 1000.00)
        self.assertEqual(product.description, "Тестовое описание букета")
        self.assertTrue(product.is_available)

    def test_average_rating_no_reviews(self):
        """Проверка среднего рейтинга продукта без отзывов."""
        self.assertIsNone(self.product.average_rating())

    def test_average_rating_with_reviews(self):
        """Проверка расчета среднего рейтинга продукта с отзывами."""
        # Создание отзывов для тестового продукта с пользователем
        Review.objects.create(product=self.product, user=self.user, rating=5, comment="Отличный букет")
        Review.objects.create(product=self.product, user=self.user, rating=3, comment="Средний букет")
        Review.objects.create(product=self.product, user=self.user, rating=4, comment="Хороший букет")

        # Проверка среднего рейтинга
        expected_average = 4  # Среднее значение: (5 + 3 + 4) / 3
        self.assertEqual(self.product.average_rating(), expected_average)

    def test_str_representation(self):
        """Проверка строкового представления продукта."""
        self.assertEqual(str(self.product), "Тестовый букет")

    def test_verbose_names(self):
        """Проверка verbose_name полей модели."""
        field_names = {
            'name': "Название",
            'price': "Цена",
            'description': "Описание",
            'image': "Изображение",
            'is_available': "В наличии",
            'created_at': "Дата добавления",
        }
        for field_name, verbose_name in field_names.items():
            field = Product._meta.get_field(field_name)
            self.assertEqual(field.verbose_name, verbose_name)

    def test_meta_options(self):
        """Проверка meta-параметров модели."""
        self.assertEqual(Product._meta.verbose_name, "Продукт")
        self.assertEqual(Product._meta.verbose_name_plural, "Продукты")
