# apps/orders/forms.py

from django import forms  # Импорт библиотеки Django для создания форм

from .models import Order  # Импорт модели Order из текущего приложения


class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказа.

    Включает поля для ввода контактных данных, даты и времени доставки, дополнительной информации,
    а также опции для получения уведомлений по электронной почте и Telegram.
    """

    # Поле для ввода контактного телефона с обязательным заполнением
    contact_phone = forms.CharField(
        required=True,
        label='Контактный телефон',
        widget=forms.TextInput(attrs={'placeholder': 'Введите контактный телефон'})  # Виджет для отображения в HTML
    )

    # Поле для ввода даты доставки с обязательным заполнением
    delivery_date = forms.DateField(
        required=True,
        label='Дата доставки',
        widget=forms.SelectDateWidget()  # Виджет для выбора даты
    )

    # Поле для ввода времени доставки с обязательным заполнением
    delivery_time = forms.TimeField(
        required=True,
        label='Время доставки',
        widget=forms.TimeInput(attrs={'type': 'time'})  # Виджет для выбора времени в HTML
    )

    # Поле для ввода дополнительной информации (необязательно)
    additional_info = forms.CharField(
        required=False,
        label='Дополнительная информация',
        widget=forms.Textarea(attrs={'placeholder': 'Введите дополнительную информацию'}),
        max_length=500  # Ограничение по количеству символов
    )

    # Чекбокс для выбора уведомлений по электронной почте
    email_notifications = forms.BooleanField(
        required=False,
        label='Получать уведомления по e-mail',
        widget=forms.CheckboxInput()  # Виджет для отображения чекбокса в HTML
    )

    # Чекбокс для выбора уведомлений по Telegram
    telegram_notifications = forms.BooleanField(
        required=False,
        label='Получать уведомления по Telegram',
        widget=forms.CheckboxInput()  # Виджет для отображения чекбокса в HTML
    )

    class Meta:
        """
        Мета-класс для определения дополнительных настроек формы.

        Определяет, какая модель используется для формы, и задает порядок отображения полей.
        """
        model = Order  # Используемая модель
        fields = [
            'delivery_address', 'contact_phone', 'delivery_date', 'delivery_time',
            'additional_info', 'email_notifications', 'telegram_notifications', 'total_price'
        ]  # Поля, отображаемые в форме
        labels = {
            'delivery_address': 'Адрес доставки',
            'contact_phone': 'Контактный телефон',
            'delivery_date': 'Дата доставки',
            'delivery_time': 'Время доставки',
            'additional_info': 'Дополнительная информация',
            'email_notifications': 'Уведомления по e-mail',
            'telegram_notifications': 'Уведомления по Telegram',
            'total_price': 'Общая стоимость',
        }  # Метки для полей, которые будут отображаться на форме
