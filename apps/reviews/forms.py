# apps/reviews/forms.py

from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']  # Убедитесь, что поля соответствуют модели Review
        labels = {
            'product': 'Продукт',
            'rating': 'Рейтинг',
            'comment': 'Комментарий',
        }
