# apps/reviews/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.reviews.views import add_review, edit_review


class ReviewURLsTest(SimpleTestCase):

    def test_add_review_url_is_resolved(self):
        """Проверка разрешения URL для добавления отзыва."""
        url = reverse('reviews:add_review', args=[1])
        self.assertEqual(resolve(url).func, add_review)

    def test_edit_review_url_is_resolved(self):
        """Проверка разрешения URL для редактирования отзыва."""
        url = reverse('reviews:edit_review', args=[1])
        self.assertEqual(resolve(url).func, edit_review)
