# apps/orders/forms.py

from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['delivery_address', 'products', 'status', 'total_price']  # Убедитесь, что поля соответствуют модели Order
        widgets = {
            'products': forms.CheckboxSelectMultiple(),  # Виджет для выбора нескольких товаров
        }
        labels = {
            'delivery_address': 'Адрес доставки',
            'products': 'Товары',
            'status': 'Статус заказа',
            'total_price': 'Общая стоимость',
        }
