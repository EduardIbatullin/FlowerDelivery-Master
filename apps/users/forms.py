# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


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

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'patronymic', 'birth_date']
