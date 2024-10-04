# apps\users\signals.py

from django.db.models.signals import post_save  # Импорт сигнала post_save для отслеживания сохранения модели
from django.dispatch import receiver  # Импорт декоратора receiver для подключения функций к сигналам

from .models import CustomUser, Profile  # Импорт моделей CustomUser и Profile из текущего приложения


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Создает профиль пользователя при создании нового пользователя.

    Функция принимает сигнал post_save от модели CustomUser. Если пользователь был создан и у него нет профиля,
    создается новый профиль, связанный с этим пользователем.

    Аргументы:
        sender: Класс модели, отправившей сигнал (CustomUser).
        instance: Экземпляр модели CustomUser, который был сохранен.
        created: Булево значение, True если новый объект был создан.
        **kwargs: Дополнительные именованные аргументы.

    Возвращает:
        None
    """
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Сохраняет профиль пользователя при сохранении пользователя.

    Функция принимает сигнал post_save от модели CustomUser. Если у пользователя есть профиль,
    то профиль сохраняется, обеспечивая обновление связанной информации.

    Аргументы:
        sender: Класс модели, отправившей сигнал (CustomUser).
        instance: Экземпляр модели CustomUser, который был сохранен.
        **kwargs: Дополнительные именованные аргументы.

    Возвращает:
        None
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
