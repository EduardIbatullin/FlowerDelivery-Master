# apps/management/forms.py

from django import forms
from apps.orders.models import Order


class OrderStatusForm(forms.ModelForm):

    """Форма для изменения статуса заказа"""

    class Meta:
        model = Order
        fields = ['status']
        labels = {
            'status': 'Выберите новый статус',
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        current_status = kwargs.pop('current_status', None)
        super(OrderStatusForm, self).__init__(*args, **kwargs)

        if self.instance.complete:
            self.fields['status'].widget.attrs['disabled'] = True


class OrderFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'Все')] + Order.STATUS_CHOICES,
        required=False,
        label="Статус заказа"
    )
    complete = forms.ChoiceField(
        choices=[('', 'Все'), ('True', 'Завершен'), ('False', 'Не завершен')],
        required=False,
        label="Завершение заказа"
    )
