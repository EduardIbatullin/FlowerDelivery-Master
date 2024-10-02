# apps/analytics/forms.py

from django import forms
from django.core.exceptions import ValidationError
from apps.catalog.models import Product


class AnalyticsFilterForm(forms.Form):
    PERIOD_CHOICES = [
        ('all_time', 'За все время'),
        ('year', 'За год'),
        ('6_months', 'За 6 месяцев'),
        ('3_months', 'За 3 месяца'),
        ('1_month', 'За месяц'),
        ('2_weeks', 'За 2 недели'),
        ('1_week', 'За неделю'),
        ('1_day', 'За день'),
        ('custom', 'Выберите период'),
    ]

    period = forms.ChoiceField(choices=PERIOD_CHOICES, required=True, label='Период')
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=False, label='Букет')
    custom_start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Начало периода')
    custom_end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Конец периода')

    def clean(self):
        cleaned_data = super().clean()
        period = cleaned_data.get('period')
        start_date = cleaned_data.get('custom_start_date')
        end_date = cleaned_data.get('custom_end_date')

        # Проверка, что конец периода не раньше начала
        if period == 'custom' and start_date and end_date:
            if end_date < start_date:
                raise ValidationError('Конец периода не может быть раньше начала.')

        return cleaned_data
