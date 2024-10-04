# apps/users/forms.py

from django import forms  # Модули для создания и обработки форм в Django
from django.contrib.auth.forms import UserCreationForm  # Базовая форма для создания пользователя

from .models import CustomUser, Profile  # Пользовательские модели для работы с формами


class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации нового пользователя с дополнительными полями.

    Расширяет стандартную форму создания пользователя, добавляя поля отчества и даты рождения.

    Поля:
        patronymic (CharField): Отчество пользователя (необязательное поле).
        birth_date (DateField): Дата рождения пользователя (необязательное поле).
    """

    patronymic = forms.CharField(required=False, label='Отчество')
    birth_date = forms.DateField(
        required=False,
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='',
    )

    class Meta:
        """
        Метаданные для настройки формы.

        Атрибуты:
            model: Модель, на основе которой создается форма.
            fields: Поля модели, которые будут включены в форму.
        """
        model = CustomUser
        fields = ('username', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    """
    Форма для редактирования профиля пользователя.

    Позволяет пользователю обновлять личную информацию и контактные данные.

    Поля:
        last_name (CharField): Фамилия пользователя (необязательное поле).
        first_name (CharField): Имя пользователя (необязательное поле).
        patronymic (CharField): Отчество пользователя (необязательное поле).
        birth_date (DateField): Дата рождения пользователя (необязательное поле).
        email (EmailField): Электронная почта пользователя (необязательное поле).
        telegram_id (CharField): Telegram ID пользователя (необязательное поле).
    """

    last_name = forms.CharField(required=False, label='Фамилия')
    first_name = forms.CharField(required=False, label='Имя')
    patronymic = forms.CharField(required=False, label='Отчество')
    birth_date = forms.DateField(
        required=False,
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    email = forms.EmailField(required=False, label='Email')
    telegram_id = forms.CharField(required=False, label='Telegram ID')

    class Meta:
        """
        Метаданные для настройки формы.

        Атрибуты:
            model: Модель, на основе которой создается форма.
            fields: Поля модели, которые будут включены в форму.
        """
        model = Profile
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date', 'email', 'telegram_id']

    def __init__(self, *args, **kwargs):
        """
        Инициализирует форму с возможностью предзаполнения полей данными пользователя.

        Если в kwargs передан пользователь, предзаполняет поля формы данными из модели пользователя и профиля.

        Аргументы:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы, могут содержать ключ 'user'.
        """
        user = kwargs.pop('user', None)
        super(UserProfileForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['last_name'].initial = user.last_name
            self.fields['first_name'].initial = user.first_name
            self.fields['patronymic'].initial = user.patronymic
            self.fields['birth_date'].initial = user.birth_date

            # Заполняем поля email и telegram_id из профиля пользователя, если они существуют
            if hasattr(user, 'profile'):
                self.fields['email'].initial = user.profile.email
                self.fields['telegram_id'].initial = user.profile.telegram_id
            else:
                self.fields['email'].initial = ''
                self.fields['telegram_id'].initial = ''

    def save(self, commit=True):
        """
        Сохраняет обновленные данные пользователя и профиля.

        Обновляет информацию в модели CustomUser и связанной модели Profile.

        Аргументы:
            commit (bool): Флаг, указывающий на необходимость сохранения в базе данных.

        Возвращает:
            Profile: Обновленный объект профиля пользователя.
        """
        user = self.instance.user
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        user.patronymic = self.cleaned_data['patronymic']
        user.birth_date = self.cleaned_data['birth_date']
        user.save()

        # Обновляем поля профиля
        profile = self.instance
        profile.email = self.cleaned_data['email']
        profile.telegram_id = self.cleaned_data['telegram_id']
        if commit:
            profile.save()
        return profile
