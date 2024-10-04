# apps/orders/models.py

from django.db import models  # Импортируем модуль моделей из Django для работы с базой данных
from django.conf import settings  # Импортируем настройки проекта для использования модели пользователя
from django.utils import timezone  # Импортируем модуль для работы с датой и временем

from apps.catalog.models import Product  # Импортируем модель Product для связи с заказами


class Order(models.Model):
    """
    Модель для хранения информации о заказе.

    Атрибуты:
        - user (ForeignKey): Ссылка на пользователя, который сделал заказ.
        - created_at (DateTimeField): Дата и время создания заказа.
        - updated_at (DateTimeField): Дата и время последнего обновления заказа.
        - status (CharField): Текущий статус заказа (например, 'В ожидании', 'Доставлен').
        - total_price (DecimalField): Общая стоимость заказа. Может быть пустым, так как вычисляется автоматически.
        - delivery_address (CharField): Адрес доставки заказа.
        - contact_phone (CharField): Контактный телефон для связи по заказу.
        - delivery_date (DateField): Дата доставки заказа.
        - delivery_time (TimeField): Время доставки заказа.
        - additional_info (TextField): Дополнительная информация к заказу.
        - email_notifications (BooleanField): Флаг для включения/отключения уведомлений по e-mail.
        - telegram_notifications (BooleanField): Флаг для включения/отключения уведомлений через Telegram.
        - complete (BooleanField): Флаг завершенности заказа.
    """

    # Определение возможных статусов заказа
    STATUS_CHOICES = [
        ('В ожидании', 'В ожидании'),
        ('В обработке', 'В обработке'),
        ('В дороге', 'В дороге'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )  # Связь с пользователем, который сделал заказ

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )  # Автоматическая дата и время создания заказа

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )  # Автоматическое обновление даты и времени при каждом изменении заказа

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='В ожидании',
        verbose_name='Статус заказа'
    )  # Статус заказа, выбор из заранее определенных вариантов

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name='Общая стоимость'
    )  # Общая стоимость заказа. Может быть пустым, так как вычисляется автоматически.

    delivery_address = models.CharField(
        max_length=255,
        verbose_name='Адрес доставки'
    )  # Адрес доставки, введенный пользователем

    contact_phone = models.CharField(
        max_length=20,
        default='',
        verbose_name='Контактный телефон'
    )  # Контактный телефон для связи по заказу

    delivery_date = models.DateField(
        verbose_name='Дата доставки',
        default=timezone.now
    )  # Дата доставки заказа

    delivery_time = models.TimeField(
        verbose_name='Время доставки',
        default=timezone.now
    )  # Время доставки заказа

    additional_info = models.TextField(
        blank=True,
        null=True,
        verbose_name='Дополнительная информация'
    )  # Дополнительная информация к заказу (необязательное поле)

    email_notifications = models.BooleanField(
        default=False,
        verbose_name='Уведомления по email'
    )  # Включение/отключение уведомлений по e-mail

    telegram_notifications = models.BooleanField(
        default=False,
        verbose_name='Уведомления по Telegram'
    )  # Включение/отключение уведомлений через Telegram

    complete = models.BooleanField(
        default=False,
        verbose_name="Заказ завершен"
    )  # Флаг завершенности заказа

    def __str__(self):
        """
        Строковое представление объекта заказа.
        Показывает идентификатор заказа и имя пользователя.
        """
        return f"Order {self.id} by {self.user}"

    def get_total_price(self):
        """
        Вычисление общей стоимости заказа на основе всех товаров в нем.

        Возвращает:
            Decimal: Суммарная стоимость всех товаров в заказе.
        """
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    """
    Промежуточная модель для хранения информации о каждом товаре в заказе.

    Атрибуты:
        - order (ForeignKey): Ссылка на заказ, к которому относится данный элемент.
        - product (ForeignKey): Ссылка на продукт (букет), который добавлен в заказ.
        - quantity (PositiveIntegerField): Количество единиц данного продукта в заказе.
        - price_at_purchase (DecimalField): Цена продукта на момент покупки.
    """

    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )  # Связь с заказом, к которому относится элемент

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )  # Связь с продуктом, добавленным в заказ

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )  # Количество единиц данного продукта в заказе

    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена при покупке'
    )  # Цена продукта на момент покупки

    def __str__(self):
        """
        Строковое представление объекта элемента заказа.
        Показывает количество и название продукта, а также идентификатор заказа.
        """
        return f"{self.quantity} x {self.product.name} для заказа {self.order.id}"

    @property
    def total_price(self):
        """
        Вычисление общей стоимости данного элемента заказа.

        Возвращает:
            Decimal: Стоимость элемента заказа (количество * цена на момент покупки).
        """
        return self.quantity * self.price_at_purchase
