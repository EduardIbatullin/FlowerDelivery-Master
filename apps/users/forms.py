# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    patronymic = forms.CharField(required=False, label='Отчество')
    birth_date = forms.DateField(
        required=False,
        label='Дата рождения',
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='',
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
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
        model = Profile  # Изменено на модель Profile
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date', 'email', 'telegram_id']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем пользователя из переданных аргументов
        super(UserProfileForm, self).__init__(*args, **kwargs)

        if user:
            # Заполняем поля данными из CustomUser
            self.fields['last_name'].initial = user.last_name
            self.fields['first_name'].initial = user.first_name
            self.fields['patronymic'].initial = user.patronymic
            self.fields['birth_date'].initial = user.birth_date

            # Заполняем поле email и telegram_id из профиля пользователя
            self.fields['email'].initial = user.profile.email if hasattr(user, 'profile') else ''
            self.fields['telegram_id'].initial = user.profile.telegram_id if hasattr(user, 'profile') else ''

    def save(self, commit=True):
        user = self.instance.user  # Получаем пользователя из instance профиля
        user.last_name = self.cleaned_data['last_name']
        user.first_name = self.cleaned_data['first_name']
        user.patronymic = self.cleaned_data['patronymic']
        user.birth_date = self.cleaned_data['birth_date']
        user.save()

        # Обновляем профильные поля
        profile = self.instance
        profile.email = self.cleaned_data['email']
        profile.telegram_id = self.cleaned_data['telegram_id']
        if commit:
            profile.save()
        return profile
