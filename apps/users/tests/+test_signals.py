# apps/users/tests/test_signals.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import Profile

User = get_user_model()


class UserProfileSignalsTest(TestCase):
    def setUp(self):
        """Подготовка тестовых данных."""
        # Создаем тестового пользователя
        self.user = User.objects.create(username='testuser', first_name='Иван', last_name='Иванов')

    def test_profile_created_on_user_creation(self):
        """Проверка создания профиля при создании пользователя."""
        # Проверяем, что профиль был создан автоматически после создания пользователя
        profile_exists = Profile.objects.filter(user=self.user).exists()
        self.assertTrue(profile_exists, "Профиль не был создан автоматически при создании пользователя")

    def test_profile_updated_on_user_save(self):
        """Проверка сохранения профиля при обновлении пользователя."""
        # Обновляем данные пользователя
        self.user.first_name = 'Обновленное имя'
        self.user.save()

        # Обновляем профиль пользователя (вызывается сигнал save_user_profile)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Обновленное имя',
                         "Профиль не был обновлен после сохранения пользователя")

    def test_no_profile_creation_for_existing_user(self):
        """Проверка, что сигнал не создает профиль повторно для существующего пользователя."""
        # Проверяем количество профилей до сохранения пользователя
        initial_profile_count = Profile.objects.count()

        # Сохраняем пользователя, что вызывает сигнал save_user_profile
        self.user.save()

        # Проверяем количество профилей после сохранения пользователя
        final_profile_count = Profile.objects.count()

        # Количество профилей не должно измениться
        self.assertEqual(initial_profile_count, final_profile_count,
                         "Сигнал создал повторный профиль для существующего пользователя")

    def test_no_error_when_profile_does_not_exist(self):
        """Проверка отсутствия ошибки, если профиль не существует при сохранении пользователя."""
        # Удаляем профиль, если он есть
        Profile.objects.filter(user=self.user).delete()

        try:
            # Сохраняем пользователя, что вызовет сигнал save_user_profile
            self.user.save()
        except Exception as e:
            self.fail(f"При сохранении пользователя возникла ошибка: {e}")
