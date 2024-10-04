# apps/analytics/forms.py

from django import forms  # Импорт модуля для создания форм в Django
from django.core.exceptions import ValidationError  # Импорт исключения для обработки ошибок валидации форм

from apps.catalog.models import Product  # Импорт модели Product из каталога для использования в фильтре


class AnalyticsFilterForm(forms.Form):
    """
    Форма фильтрации для аналитики по продажам.

    Форма позволяет выбрать период времени и конкретный букет для получения аналитических данных.
    Включает предустановленные значения периода времени и возможность указать произвольный временной промежуток.

    Атрибуты:
        PERIOD_CHOICES (list of tuple): Список предустановленных вариантов периода времени.
        period (ChoiceField): Поле выбора периода времени для отображения данных.
        product (ModelChoiceField): Поле для выбора конкретного букета (опционально).
        custom_start_date (DateField): Поле для указания произвольной даты начала периода.
        custom_end_date (DateField): Поле для указания произвольной даты окончания периода.
    """

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
        """
        Валидатор формы.

        Проверяет корректность введенных данных:
        - Если выбран произвольный период ('custom'), то проверяет, чтобы конец периода не был раньше начала.
        - В случае некорректных данных вызывает ошибку валидации.

        Возвращает:
            cleaned_data (dict): Очищенные данные формы, готовые к дальнейшей обработке.
        """
        cleaned_data = super().clean()
        period = cleaned_data.get('period')
        start_date = cleaned_data.get('custom_start_date')
        end_date = cleaned_data.get('custom_end_date')

        if period == 'custom' and start_date and end_date and end_date < start_date:
            raise ValidationError('Конец периода не может быть раньше начала.')

        return cleaned_data
