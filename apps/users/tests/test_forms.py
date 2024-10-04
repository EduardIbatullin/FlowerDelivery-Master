# apps/users/tests/test_forms.py

from datetime import date  # Импорт модуля для работы с датами

from django.test import TestCase  # Импорт базового класса TestCase для создания тестов Django

from apps.users.forms import CustomUserCreationForm, \
    UserProfileForm  # Импорт тестируемых форм: регистрация и профиль пользователя
from apps.users.models import CustomUser, Profile  # Импорт моделей пользователя и профиля


class CustomUserCreationFormTest(TestCase):
    """
    Набор тестов для проверки формы `CustomUserCreationForm`.

    Тестируемые сценарии:
    1. Валидация формы с корректными данными.
    """

    def test_form_valid_data(self):
        """
        Проверка формы регистрации пользователя с корректными данными.

        Убеждается, что форма корректно валидируется и данные пользователя сохраняются правильно.

        Входные данные:
            - username: 'testuser'.
            - password1: 'strongpassword123'.
            - password2: 'strongpassword123'.
            - patronymic: 'Иванович'.
            - birth_date: '1990-01-01'.

        Ожидаемый результат:
            - Форма валидна.
            - Данные формы совпадают с переданными значениями.
        """
        form_data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'patronymic': 'Иванович',
            'birth_date': '1990-01-01'
        }
        form = CustomUserCreationForm(data=form_data)  # Инициализация формы с тестовыми данными
        self.assertTrue(form.is_valid())  # Проверка, что форма валидируется корректно
        self.assertEqual(form.cleaned_data['username'], 'testuser')  # Проверка поля username
        self.assertEqual(form.cleaned_data['patronymic'], 'Иванович')  # Проверка поля patronymic
        self.assertEqual(form.cleaned_data['birth_date'], date(1990, 1, 1))  # Проверка поля birth_date


class UserProfileFormTest(TestCase):
    """
    Набор тестов для проверки формы `UserProfileForm`.

    Тестируемые сценарии:
    1. Валидация формы с корректными данными.
    2. Валидация формы с отсутствующими необязательными полями.
    3. Валидация формы с пустым полем Telegram ID.
    4. Валидация формы с отсутствующими обязательными полями.
    """

    def setUp(self):
        """
        Создание тестового пользователя и профиля для проверки формы профиля.

        Устанавливает начальные данные для всех тестов в классе.

        Входные данные:
            - username: 'testuser'.
            - first_name: 'Иван'.
            - last_name: 'Иванов'.
            - email: 'testuser@example.com'.
            - telegram_id: '123456789'.
        """
        self.user = CustomUser.objects.create(username='testuser', first_name='Иван', last_name='Иванов')

        # Удаляем существующий профиль пользователя, если он есть
        Profile.objects.filter(user=self.user).delete()

        # Создаем профиль для пользователя
        self.profile = Profile.objects.create(user=self.user, email='testuser@example.com', telegram_id='123456789')

    def test_profile_form_valid_data(self):
        """
        Проверка формы профиля с корректными данными.

        Убеждается, что форма валидируется и обновляет профиль пользователя.

        Входные данные:
            - last_name: 'Иванов'.
            - first_name: 'Иван'.
            - patronymic: 'Иванович'.
            - birth_date: '1990-01-01'.
            - email: 'testuser@example.com'.
            - telegram_id: '123456789'.

        Ожидаемый результат:
            - Форма валидна.
            - Профиль пользователя обновлен корректными данными.
        """
        form_data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
            'birth_date': '1990-01-01',
            'email': 'testuser@example.com',
            'telegram_id': '123456789'
        }
        form = UserProfileForm(data=form_data, instance=self.profile)  # Инициализация формы с данными профиля
        self.assertTrue(form.is_valid())  # Проверка, что форма валидируется
        updated_profile = form.save()  # Сохранение формы и обновление профиля
        self.assertEqual(updated_profile.user.last_name, 'Иванов')  # Проверка обновленного поля last_name
        self.assertEqual(updated_profile.user.first_name, 'Иван')  # Проверка обновленного поля first_name
        self.assertEqual(updated_profile.user.patronymic, 'Иванович')  # Проверка обновленного поля patronymic
        self.assertEqual(updated_profile.user.birth_date.strftime('%Y-%m-%d'), '1990-01-01')  # Проверка birth_date
        self.assertEqual(updated_profile.email, 'testuser@example.com')  # Проверка обновленного email
        self.assertEqual(updated_profile.telegram_id, '123456789')  # Проверка обновленного Telegram ID

    def test_profile_form_missing_non_required_fields(self):
        """
        Проверка формы профиля с отсутствующими необязательными полями.

        Убеждается, что форма корректно обрабатывает отсутствие необязательных данных.

        Входные данные:
            - last_name: ''.
            - first_name: ''.
            - patronymic: ''.
            - birth_date: ''.
            - email: ''.
            - telegram_id: ''.

        Ожидаемый результат:
            - Форма валидна.
            - Обновленный профиль имеет пустые значения для необязательных полей.
        """
        form_data = {
            'last_name': '',
            'first_name': '',
            'patronymic': '',
            'birth_date': '',
            'email': '',
            'telegram_id': ''
        }
        form = UserProfileForm(data=form_data, instance=self.profile)  # Инициализация формы с отсутствующими данными
        self.assertTrue(form.is_valid())  # Проверка, что форма валидируется
        updated_profile = form.save()  # Сохранение формы и обновление профиля
        self.assertEqual(updated_profile.user.last_name, '')  # Проверка пустого поля last_name
        self.assertEqual(updated_profile.user.first_name, '')  # Проверка пустого поля first_name
        self.assertEqual(updated_profile.user.patronymic, '')  # Проверка пустого поля patronymic
        self.assertIsNone(updated_profile.user.birth_date)  # Проверка пустого поля birth_date
        self.assertEqual(updated_profile.email, '')  # Проверка пустого поля email
        self.assertEqual(updated_profile.telegram_id, '')  # Проверка пустого поля telegram_id

    def test_profile_form_empty_telegram_id(self):
        """
        Проверка формы профиля с пустым полем Telegram ID.

        Убеждается, что форма корректно обрабатывает пустое значение Telegram ID.

        Входные данные:
            - last_name: 'Иванов'.
            - first_name: 'Иван'.
            - patronymic: 'Иванович'.
            - birth_date: '1990-01-01'.
            - email: 'testuser@example.com'.
            - telegram_id: ''.

        Ожидаемый результат:
            - Форма валидна.
            - Поле Telegram ID в обновленном профиле пустое.
        """
        form_data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': 'Иванович',
            'birth_date': '1990-01-01',
            'email': 'testuser@example.com',
            'telegram_id': ''
        }
        form = UserProfileForm(data=form_data, instance=self.profile)  # Инициализация формы с пустым Telegram ID
        self.assertTrue(form.is_valid())  # Проверка, что форма валидируется
        updated_profile = form.save()  # Сохранение формы и обновление профиля
        self.assertEqual(updated_profile.telegram_id, '')  # Проверка пустого значения Telegram ID

    def test_profile_form_missing_required_fields(self):
        """
        Проверка формы профиля без обязательных полей пользователя.

        Убеждается, что форма валидируется и сохраняет профиль без обязательных полей.

        Входные данные:
            - last_name: 'Иванов'.
            - first_name: 'Иван'.
            - patronymic: ''.
            - birth_date: ''.
            - email: 'testuser@example.com'.
            - telegram_id: ''.

        Ожидаемый результат:
            - Форма валидна.
            - Профиль сохраняется без указания обязательных полей пользователя.
        """
        form_data = {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'patronymic': '',
            'birth_date': '',
            'email': 'testuser@example.com',
            'telegram_id': ''
        }
        form = UserProfileForm(data=form_data,
                               instance=self.profile)  # Инициализация формы с отсутствующими обязательными полями
        self.assertTrue(form.is_valid())  # Проверка, что форма валидируется
        updated_profile = form.save()  # Сохранение формы и обновление профиля
        self.assertEqual(updated_profile.user.last_name, 'Иванов')  # Проверка поля last_name
        self.assertEqual(updated_profile.user.first_name, 'Иван')  # Проверка поля first_name
