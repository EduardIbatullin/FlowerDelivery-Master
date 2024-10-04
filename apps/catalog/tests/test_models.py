# apps/catalog/tests/test_models.py

from django.contrib.auth import get_user_model  # Импорт функции для получения пользовательской модели
from django.test import TestCase  # Импорт TestCase для создания и выполнения тестов

from apps.catalog.models import Product  # Импорт модели Product для работы с тестируемыми данными
from apps.reviews.models import Review  # Импорт модели Review для работы с отзывами на продукты

# Получение пользовательской модели для создания тестовых пользователей
User = get_user_model()


class ProductModelTest(TestCase):
    """
    Тесты для проверки модели `Product` в приложении каталога.

    Тестируемые сценарии:
    1. Создание продукта и проверка его полей.
    2. Расчет среднего рейтинга продукта без отзывов.
    3. Расчет среднего рейтинга продукта с отзывами.
    4. Проверка строкового представления (`__str__`) продукта.
    5. Проверка `verbose_name` полей модели.
    6. Проверка мета-параметров модели.
    """

    def setUp(self):
        """
        Устанавливает начальные данные для тестов.

        Создает тестового пользователя и тестовый продукт.
        """
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='password123')

        # Создаем тестовый продукт
        self.product = Product.objects.create(
            name="Тестовый букет",
            price=1000.00,
            description="Тестовое описание букета",
            is_available=True,
        )

    def test_product_creation(self):
        """
        Проверка создания продукта и его полей.

        Проверяет корректность заполнения полей `name`, `price`, `description` и `is_available`.
        """
        product = Product.objects.get(name="Тестовый букет")  # Получаем продукт по названию
        self.assertEqual(product.name, "Тестовый букет")  # Проверяем корректность названия
        self.assertEqual(product.price, 1000.00)  # Проверяем корректность цены
        self.assertEqual(product.description, "Тестовое описание букета")  # Проверяем корректность описания
        self.assertTrue(product.is_available)  # Проверяем доступность продукта

    def test_average_rating_no_reviews(self):
        """
        Проверка среднего рейтинга продукта без отзывов.

        Убеждается, что при отсутствии отзывов метод `average_rating` возвращает None.
        """
        self.assertIsNone(self.product.average_rating())  # Ожидаем None при отсутствии отзывов

    def test_average_rating_with_reviews(self):
        """
        Проверка расчета среднего рейтинга продукта с отзывами.

        Создает несколько отзывов и проверяет, что метод `average_rating` корректно рассчитывает среднее значение.
        """
        # Создание отзывов для тестового продукта
        Review.objects.create(product=self.product, user=self.user, rating=5, comment="Отличный букет")
        Review.objects.create(product=self.product, user=self.user, rating=3, comment="Средний букет")
        Review.objects.create(product=self.product, user=self.user, rating=4, comment="Хороший букет")

        # Ожидаемое среднее значение: (5 + 3 + 4) / 3 = 4
        expected_average = 4
        self.assertEqual(self.product.average_rating(), expected_average)  # Проверяем расчет среднего рейтинга

    def test_str_representation(self):
        """
        Проверка строкового представления продукта (`__str__`).

        Убеждается, что метод `__str__` возвращает корректное название продукта.
        """
        self.assertEqual(str(self.product), "Тестовый букет")  # Проверяем строковое представление

    def test_verbose_names(self):
        """
        Проверка `verbose_name` полей модели.

        Убеждается, что каждое поле модели `Product` имеет правильное описание (`verbose_name`).
        """
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
            self.assertEqual(field.verbose_name, verbose_name)  # Проверяем описание каждого поля

    def test_meta_options(self):
        """
        Проверка мета-параметров модели.

        Убеждается, что модель имеет правильные мета-описания (`verbose_name` и `verbose_name_plural`).
        """
        self.assertEqual(Product._meta.verbose_name, "Продукт")  # Проверка verbose_name
        self.assertEqual(Product._meta.verbose_name_plural, "Продукты")  # Проверка verbose_name_plural
