# apps/orders/forms.py

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    contact_phone = forms.CharField(
        required=True,
        label='Контактный телефон',
        widget=forms.TextInput(attrs={'placeholder': 'Введите контактный телефон'})
    )
    delivery_date = forms.DateField(
        required=True,
        label='Дата доставки',
        widget=forms.SelectDateWidget()
    )
    delivery_time = forms.TimeField(
        required=True,
        label='Время доставки',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    additional_info = forms.CharField(
        required=False,
        label='Дополнительная информация',
        widget=forms.Textarea(attrs={'placeholder': 'Введите дополнительную информацию'}),
        max_length=500
    )
    email_notifications = forms.BooleanField(
        required=False,
        label='Получать уведомления по e-mail',
        widget=forms.CheckboxInput()
    )
    telegram_notifications = forms.BooleanField(
        required=False,
        label='Получать уведомления по Telegram',
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Order
        fields = ['delivery_address', 'contact_phone', 'delivery_date', 'delivery_time', 'additional_info', 'email_notifications', 'telegram_notifications', 'total_price']
        labels = {
            'delivery_address': 'Адрес доставки',
            'contact_phone': 'Контактный телефон',
            'delivery_date': 'Дата доставки',
            'delivery_time': 'Время доставки',
            'additional_info': 'Дополнительная информация',
            'email_notifications': 'Уведомления по e-mail',
            'telegram_notifications': 'Уведомления по Telegram',
            'total_price': 'Общая стоимость',
        }
