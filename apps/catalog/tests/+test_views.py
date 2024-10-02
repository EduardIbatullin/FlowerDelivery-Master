# apps/catalog/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model  # Импорт кастомной модели пользователя
from apps.catalog.models import Product

User = get_user_model()  # Получение кастомной модели пользователя из настроек


class CatalogViewsTest(TestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Создание тестовых продуктов
        self.product_1 = Product.objects.create(name='Розы красные', price=3000.00,
                                                description='Красные розы для любимых', is_available=True)
        self.product_2 = Product.objects.create(name='Орхидеи', price=5000.00, description='Белые орхидеи',
                                                is_available=True)

    def test_catalog_list_view(self):
        """Тест отображения списка товаров в каталоге"""
        url = reverse('catalog:catalog_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/catalog_list.html')
        self.assertContains(response, self.product_1.name)
        self.assertContains(response, self.product_2.name)
        self.assertIn('products', response.context)
        self.assertEqual(len(response.context['products']), 2)  # Убедитесь, что два продукта в контексте

    def test_product_detail_view(self):
        """Тест отображения детального описания продукта"""
        url = reverse('catalog:product_detail', args=[self.product_1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_detail.html')
        self.assertContains(response, self.product_1.name)
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'], self.product_1)
        self.assertIn('reviews', response.context)  # Проверка наличия отзывов в контексте
        self.assertIn('form', response.context)  # Проверка наличия формы для добавления отзыва
