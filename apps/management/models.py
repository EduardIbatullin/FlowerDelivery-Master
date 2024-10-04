# apps/management/models.py

from django.db import models  # Импорт модуля для работы с моделями Django
from django.utils import timezone  # Импорт модуля для работы с датой и временем
from django.contrib.auth import get_user_model  # Импорт функции для получения кастомной модели пользователя

from apps.orders.models import Order  # Импорт модели заказа для установления связи с историей заказов

# Получение кастомной модели пользователя
User = get_user_model()


class OrderStatusHistory(models.Model):
    """
    Модель для хранения истории изменения статусов заказов.

    Данная модель отслеживает все изменения статусов для каждого заказа.
    Каждый раз, когда статус заказа изменяется, создается новая запись в этой таблице,
    что позволяет в дальнейшем просматривать историю изменений.

    Поля:
        - order (ForeignKey): Связь с моделью заказа, для которого сохраняется история.
        - previous_status (CharField): Предыдущий статус заказа до изменения.
        - new_status (CharField): Новый статус заказа после изменения.
        - changed_by (ForeignKey): Пользователь, который инициировал изменение статуса (например, администратор).
        - changed_at (DateTimeField): Время и дата, когда произошло изменение статуса.
    """
    order = models.ForeignKey(
        Order,
        related_name='status_history',
        on_delete=models.CASCADE,  # Удаление истории, если удаляется заказ
        verbose_name="Заказ"
    )
    previous_status = models.CharField(
        max_length=50,
        verbose_name="Предыдущий статус"
    )
    new_status = models.CharField(
        max_length=50,
        verbose_name="Новый статус"
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # При удалении пользователя, установится null
        null=True,
        verbose_name="Изменено пользователем"
    )
    changed_at = models.DateTimeField(
        default=timezone.now,  # По умолчанию устанавливается текущее время изменения
        verbose_name="Дата изменения"
    )

    def __str__(self):
        """
        Метод строкового представления модели.

        Возвращает строку, содержащую информацию об изменении статуса заказа,
        включая номер заказа, старый и новый статус, а также пользователя, который внес изменения.
        """
        return f"Заказ #{self.order.id}: {self.previous_status} → {self.new_status} (Изменено: {self.changed_by})"

    class Meta:
        """
        Мета-класс для модели `OrderStatusHistory`.

        Параметры:
            - verbose_name: Отображаемое имя модели в единственном числе.
            - verbose_name_plural: Отображаемое имя модели во множественном числе.
        """
        verbose_name = "История изменения заказа"
        verbose_name_plural = "История изменения заказов"
