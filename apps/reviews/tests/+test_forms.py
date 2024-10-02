# apps/reviews/tests/test_forms.py

from django.test import SimpleTestCase
from apps.reviews.forms import ReviewForm


class ReviewFormTest(SimpleTestCase):

    def test_form_fields(self):
        """Проверка наличия полей в форме."""
        form = ReviewForm()
        self.assertEqual(list(form.fields.keys()), ['rating', 'comment'])

    def test_form_valid_data(self):
        """Проверка формы с валидными данными."""
        form_data = {'rating': 4, 'comment': 'Хороший букет, всем доволен!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_rating(self):
        """Проверка формы с невалидным значением поля rating."""
        form_data = {'rating': 6, 'comment': 'Отличный букет!'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_empty_rating(self):
        """Проверка формы с пустым полем rating."""
        form_data = {'rating': '', 'comment': 'Отличный букет!'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_empty_comment(self):
        """Проверка формы с пустым полем comment."""
        form_data = {'rating': 3, 'comment': ''}
        form = ReviewForm(data=form_data)
        # Ожидаем, что форма будет валидна с пустым комментарием
        self.assertTrue(form.is_valid())

    def test_widgets(self):
        """Проверка виджетов формы."""
        form = ReviewForm()
        self.assertEqual(form.fields['rating'].widget.__class__.__name__, 'Select')
        self.assertEqual(form.fields['comment'].widget.__class__.__name__, 'Textarea')
