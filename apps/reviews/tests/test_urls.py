# apps/reviews/tests/test_urls.py

from django.test import SimpleTestCase  # Импорт базового класса для простых тестов без необходимости доступа к базе данных
from django.urls import reverse, resolve  # Импорт функций для работы с URL-адресами и их разрешения

from apps.reviews.views import add_review, edit_review  # Импорт представлений для проверки маршрутов


class ReviewURLsTest(SimpleTestCase):
    """
    Набор тестов для проверки URL-маршрутов в приложении reviews.

    Тестируемые сценарии:
    1. Проверка разрешения URL для добавления отзыва.
    2. Проверка разрешения URL для редактирования отзыва.
    """

    def test_add_review_url_is_resolved(self):
        """
        Проверяет, что URL для добавления отзыва корректно разрешается в представление `add_review`.

        Использует функцию `reverse` для генерации URL по имени маршрута и `resolve` для проверки соответствия представления.
        """
        url = reverse('reviews:add_review', args=[1])  # Генерируем URL для добавления отзыва с `product_id=1`
        self.assertEqual(resolve(url).func, add_review)  # Проверяем, что URL разрешается в функцию `add_review`

    def test_edit_review_url_is_resolved(self):
        """
        Проверяет, что URL для редактирования отзыва корректно разрешается в представление `edit_review`.

        Использует функцию `reverse` для генерации URL по имени маршрута и `resolve` для проверки соответствия представления.
        """
        url = reverse('reviews:edit_review', args=[1])  # Генерируем URL для редактирования отзыва с `review_id=1`
        self.assertEqual(resolve(url).func, edit_review)  # Проверяем, что URL разрешается в функцию `edit_review`
