# apps/users/tests/test_forms.py

from django.test import TestCase
from apps.users.forms import CustomUserCreationForm, UserProfileForm
from apps.users.models import CustomUser, Profile
from datetime import date


class CustomUserCreationFormTest(TestCase):
    def test_form_valid_data(self):
        """Проверка формы регистрации пользователя с корректными данными."""
        form_data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'patronymic': 'Иванович',
            'birth_date': '1990-01-01'
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['username'], 'testuser')
        self.assertEqual(form.cleaned_data['patronymic'], 'Иванович')
        self.assertEqual(form.cleaned_data['birth_date'], date(1990, 1, 1))


class UserProfileFormTest(TestCase):
    def setUp(self):
        """Создание тестового пользователя и профиля для проверки формы профиля."""
        # Создаем пользователя
        self.user = CustomUser.objects.create(username='testuser', first_name='Иван', last_name='Иванов')

        # Если у пользователя уже есть профиль, удаляем его перед созданием нового
        Profile.objects.filter(user=self.user).delete()
        # Создаем профиль для пользователя
        self.profile = Profile.objects.create(user=self.user, email='testuser@example.com', telegram_id='123456789')

    def test_profile_form_valid_data(self):
        """Проверка формы профиля с корректными данными."""
        form_data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
            'birth_date': '1990-01-01',
            'email': 'testuser@example.com',
            'telegram_id': '123456789'
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.user.last_name, 'Иванов')
        self.assertEqual(updated_profile.user.first_name, 'Иван')
        self.assertEqual(updated_profile.user.patronymic, 'Иванович')
        self.assertEqual(updated_profile.user.birth_date.strftime('%Y-%m-%d'), '1990-01-01')
        self.assertEqual(updated_profile.email, 'testuser@example.com')
        self.assertEqual(updated_profile.telegram_id, '123456789')

    def test_profile_form_missing_non_required_fields(self):
        """Проверка формы профиля без необязательных полей."""
        form_data = {
            'last_name': '',
            'first_name': '',
            'patronymic': '',
            'birth_date': '',
            'email': '',
            'telegram_id': ''
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.user.last_name, '')
        self.assertEqual(updated_profile.user.first_name, '')
        self.assertEqual(updated_profile.user.patronymic, '')
        self.assertIsNone(updated_profile.user.birth_date)
        self.assertEqual(updated_profile.email, '')
        self.assertEqual(updated_profile.telegram_id, '')

    def test_profile_form_empty_telegram_id(self):
        """Проверка формы профиля с пустым полем Telegram ID."""
        form_data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
            'birth_date': '1990-01-01',
            'email': 'testuser@example.com',
            'telegram_id': ''
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.telegram_id, '')  # Поле Telegram ID должно быть пустым

    def test_profile_form_missing_required_fields(self):
        """Проверка формы профиля без обязательных полей пользователя."""
        form_data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': '',
            'birth_date': '',
            'email': 'testuser@example.com',
            'telegram_id': ''
        }
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
        updated_profile = form.save()
        self.assertEqual(updated_profile.user.last_name, 'Иванов')
        self.assertEqual(updated_profile.user.first_name, 'Иван')
