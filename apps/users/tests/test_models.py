# apps/users/tests/test_models.py

from datetime import date  # Импорт модуля для работы с датами

from django.test import TestCase  # Импорт базового класса для создания тестов Django

from apps.users.models import CustomUser, Profile  # Импорт тестируемых моделей пользователя и профиля


class CustomUserModelTest(TestCase):
    """
    Набор тестов для проверки модели `CustomUser`.

    Тестируемые сценарии:
    1. Создание пользователя с заданными данными.
    2. Проверка строкового представления пользователя.
    """

    def setUp(self):
        """
        Создание тестового пользователя для тестирования.

        Устанавливает начальные данные для всех тестов в классе.

        Входные данные:
            - username: 'testuser'.
            - first_name: 'Иван'.
            - last_name: 'Иванов'.
            - patronymic: 'Иванович'.
            - birth_date: date(1990, 1, 1).
        """
        self.user = CustomUser.objects.create(
            username='testuser',
            first_name='Иван',
            last_name='Иванов',
            patronymic='Иванович',
            birth_date=date(1990, 1, 1)  # Используем объект date для даты рождения
        )

    def test_create_user(self):
        """
        Проверка создания пользователя с заданными данными.

        Убеждается, что пользователь создается с корректными данными.

        Ожидаемый результат:
            - Пользователь имеет заданные значения для всех полей.
        """
        self.assertEqual(self.user.username, 'testuser')  # Проверка поля username
        self.assertEqual(self.user.first_name, 'Иван')  # Проверка поля first_name
        self.assertEqual(self.user.last_name, 'Иванов')  # Проверка поля last_name
        self.assertEqual(self.user.patronymic, 'Иванович')  # Проверка поля patronymic
        self.assertEqual(self.user.birth_date, date(1990, 1, 1))  # Проверка поля birth_date

    def test_user_str_representation(self):
        """
        Проверка строкового представления пользователя.

        Убеждается, что метод `__str__()` возвращает имя пользователя.

        Ожидаемый результат:
            - Строковое представление равно username пользователя.
        """
        self.assertEqual(str(self.user), 'testuser')  # Проверка строкового представления пользователя


class ProfileModelTest(TestCase):
    """
    Набор тестов для проверки модели `Profile`.

    Тестируемые сценарии:
    1. Создание профиля для пользователя.
    2. Проверка строкового представления профиля.
    3. Проверка отношения профиля к пользователю.
    """

    def setUp(self):
        """
        Создание тестового пользователя и профиля для проверки.

        Устанавливает начальные данные для всех тестов в классе.

        Входные данные:
            - username: 'testuser'.
            - first_name: 'Иван'.
            - last_name: 'Иванов'.
            - profile.delivery_address: 'Тестовый адрес'.
            - profile.phone: '1234567890'.
            - profile.email: 'testuser@example.com'.
            - profile.telegram_id: '123456789'.
        """
        self.user = CustomUser.objects.create(username='testuser', first_name='Иван', last_name='Иванов')

        # Получаем автоматически созданный профиль пользователя и обновляем его данные
        self.profile = self.user.profile
        self.profile.delivery_address = 'Тестовый адрес'
        self.profile.phone = '1234567890'
        self.profile.email = 'testuser@example.com'
        self.profile.telegram_id = '123456789'
        self.profile.save()

    def test_create_profile(self):
        """
        Проверка создания профиля для пользователя.

        Убеждается, что профиль создается и имеет корректные значения полей.

        Ожидаемый результат:
            - Профиль имеет правильные значения для всех полей.
        """
        self.assertEqual(self.profile.user.username, 'testuser')  # Проверка отношения профиля к пользователю
        self.assertEqual(self.profile.delivery_address, 'Тестовый адрес')  # Проверка поля delivery_address
        self.assertEqual(self.profile.phone, '1234567890')  # Проверка поля phone
        self.assertEqual(self.profile.email, 'testuser@example.com')  # Проверка поля email
        self.assertEqual(self.profile.telegram_id, '123456789')  # Проверка поля telegram_id

    def test_profile_str_representation(self):
        """
        Проверка строкового представления профиля.

        Убеждается, что метод `__str__()` возвращает строку вида 'Profile of <username>'.

        Ожидаемый результат:
            - Строковое представление равно 'Profile of <username>'.
        """
        self.assertEqual(str(self.profile), f'Profile of {self.user.username}')  # Проверка строкового представления профиля

    def test_profile_user_relation(self):
        """
        Проверка отношения профиля к пользователю.

        Убеждается, что у пользователя есть профиль и он соответствует текущему пользователю.

        Ожидаемый результат:
            - Профиль пользователя связан с правильным экземпляром CustomUser.
        """
        self.assertEqual(self.user.profile, self.profile)  # Проверка отношения профиля к пользователю
