# apps/users/models.py

from django.contrib.auth.models import AbstractUser  # Импорт базовой пользовательской модели Django
from django.db import models  # Импорт модуля моделей Django для создания пользовательских моделей


class CustomUser(AbstractUser):
    """
    Расширенная пользовательская модель на основе AbstractUser.

    Добавляет дополнительные поля для хранения отчества и даты рождения пользователя.

    Поля:
        patronymic (CharField): Отчество пользователя (необязательное поле).
        birth_date (DateField): Дата рождения пользователя (необязательное поле).
    """

    patronymic = models.CharField(max_length=150, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        """
        Возвращает строковое представление пользователя.

        Возвращает:
            str: Имя пользователя (username).
        """
        return self.username


class Profile(models.Model):
    """
    Модель профиля пользователя, связанная с CustomUser через отношение один-к-одному.

    Хранит дополнительную информацию о пользователе, такую как адрес доставки, телефон и контакты.

    Поля:
        user (OneToOneField): Ссылка на связанного пользователя.
        delivery_address (CharField): Адрес доставки пользователя (необязательное поле).
        phone (CharField): Номер телефона пользователя (необязательное поле).
        email (EmailField): Электронная почта пользователя (необязательное поле).
        telegram_id (CharField): Telegram ID пользователя (необязательное поле).
    """

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        """
        Возвращает строковое представление профиля пользователя.

        Возвращает:
            str: Строка в формате 'Profile of <username>'.
        """
        return f'Profile of {self.user.username}'
