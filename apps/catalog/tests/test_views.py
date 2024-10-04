# apps/catalog/tests/test_views.py

from django.contrib.auth import get_user_model  # Импорт кастомной модели пользователя для создания тестовых пользователей
from django.test import TestCase  # Импорт класса TestCase для создания тестов с использованием базы данных
from django.urls import reverse  # Импорт функции для формирования URL по имени маршрута

from apps.catalog.models import Product  # Импорт модели Product для создания тестовых продуктов

User = get_user_model()  # Получение пользовательской модели из настроек проекта


class CatalogViewsTest(TestCase):
    """
    Тесты для проверки представлений (views) приложения каталога.

    Тестируемые сценарии:
    1. Проверка отображения списка товаров в каталоге.
    2. Проверка отображения детальной информации о конкретном товаре.
    """

    def setUp(self):
        """
        Установка начальных данных для тестов.

        Создаются тестовый пользователь и два продукта, которые будут использоваться
        во всех тестах данного класса.
        """
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Создание тестовых продуктов, которые будут отображаться в каталоге
        self.product_1 = Product.objects.create(
            name='Розы красные',
            price=3000.00,
            description='Красные розы для любимых',
            is_available=True
        )
        self.product_2 = Product.objects.create(
            name='Орхидеи',
            price=5000.00,
            description='Белые орхидеи',
            is_available=True
        )

    def test_catalog_list_view(self):
        """
        Тест отображения списка товаров в каталоге.

        Проверяет, что представление списка товаров возвращает корректный статус,
        использует нужный шаблон и отображает все продукты, присутствующие в базе данных.
        """
        url = reverse('catalog:catalog_list')  # Генерация URL для списка товаров
        response = self.client.get(url)

        # Проверка успешного ответа (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(response, 'catalog/catalog_list.html')

        # Проверка отображения названий продуктов в контенте страницы
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_2.name)

        # Проверка наличия списка товаров в контексте и их количества
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 2)  # Должно быть два продукта в контексте

    def test_product_detail_view(self):
        """
        Тест отображения детального описания продукта.

        Проверяет, что представление детальной страницы продукта возвращает корректный статус,
        использует нужный шаблон и отображает информацию о конкретном продукте.
        """
        url = reverse('catalog:product_detail', args=[self.product_1.pk])  # Генерация URL для детальной страницы продукта
        response = self.client.get(url)

        # Проверка успешного ответа (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(response, 'catalog/product_detail.html')

        # Проверка наличия информации о продукте на странице
        self.assertContains(response, self.product_1.name)

        # Проверка наличия ключей 'product', 'reviews' и 'form' в контексте шаблона
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product_1)
        self.assertIn('reviews', response.context)  # Отзывы должны быть переданы в контексте
        self.assertIn('form', response.context)  # Форма для добавления отзывов должна быть в контексте
