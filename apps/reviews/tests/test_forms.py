# apps/reviews/tests/test_forms.py

from django.test import SimpleTestCase  # Импорт базового класса для простых тестов без базы данных

from apps.reviews.forms import ReviewForm  # Импорт формы ReviewForm для тестирования


class ReviewFormTest(SimpleTestCase):
    """
    Набор тестов для проверки формы `ReviewForm` в приложении reviews.

    Тестируемые сценарии:
    1. Проверка наличия необходимых полей в форме.
    2. Проверка валидности формы с корректными данными.
    3. Проверка формы с невалидным значением поля `rating`.
    4. Проверка формы с пустым полем `rating`.
    5. Проверка формы с пустым полем `comment`.
    6. Проверка использования правильных виджетов в полях формы.
    """

    def test_form_fields(self):
        """
        Проверяет, что форма содержит только поля `rating` и `comment`.

        Убеждается, что никакие дополнительные поля не добавлены или не удалены.
        """
        form = ReviewForm()
        self.assertEqual(list(form.fields.keys()), ['rating', 'comment'])

    def test_form_valid_data(self):
        """
        Проверяет валидность формы при корректных данных.

        Убеждается, что форма является валидной, если предоставлены допустимые значения для всех полей.
        """
        form_data = {'rating': 4, 'comment': 'Хороший букет, всем доволен!'}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_rating(self):
        """
        Проверяет форму с недопустимым значением поля `rating`.

        Убеждается, что форма не является валидной, если значение `rating` выходит за пределы 1-5.
        """
        form_data = {'rating': 6, 'comment': 'Отличный букет!'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_empty_rating(self):
        """
        Проверяет форму с пустым полем `rating`.

        Убеждается, что форма не является валидной без указания оценки.
        """
        form_data = {'rating': '', 'comment': 'Отличный букет!'}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_form_empty_comment(self):
        """
        Проверяет форму с пустым полем `comment`.

        Убеждается, что форма остается валидной, даже если комментарий не предоставлен.
        """
        form_data = {'rating': 3, 'comment': ''}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_widgets(self):
        """
        Проверяет, что форма использует правильные виджеты для полей.

        Убеждается, что для поля `rating` используется `Select`, а для `comment` — `Textarea`.
        """
        form = ReviewForm()
        self.assertEqual(form.fields['rating'].widget.__class__.__name__, 'Select')
        self.assertEqual(form.fields['comment'].widget.__class__.__name__, 'Textarea')
