# apps/analytics/models.py

from django.db import models  # Импорт модулей для работы с моделями Django

from apps.catalog.models import Product  # Импорт модели Product для создания связи с аналитическими данными


class SalesAnalytics(models.Model):
    """
    Модель для хранения аналитических данных по продажам букетов.

    Хранит информацию о продажах каждого букета за указанный период, включая общее количество продаж,
    общую выручку и среднюю стоимость заказа.

    Атрибуты:
        product (ForeignKey): Связь с моделью `Product` из каталога. Указывает, для какого букета собирается аналитика.
        total_sales (IntegerField): Общее количество проданных букетов за указанный период.
        total_revenue (DecimalField): Общая выручка за указанный период.
        average_order_value (DecimalField): Средняя стоимость заказа за указанный период.
        period_start (DateField): Дата начала отчетного периода.
        period_end (DateField): Дата окончания отчетного периода.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales_analytics', verbose_name='Букет')
    total_sales = models.IntegerField(default=0, verbose_name='Общее количество продаж')
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Общая выручка')
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Средняя стоимость заказа')
    period_start = models.DateField(verbose_name='Начало периода')
    period_end = models.DateField(verbose_name='Конец периода')

    def __str__(self) -> str:
        """
        Строковое представление модели.

        Возвращает:
            str: Описание аналитики продаж для конкретного букета и периода времени.
        """
        return f"Аналитика продаж: {self.product.name} ({self.period_start} - {self.period_end})"

    class Meta:
        """
        Метаданные модели.

        Определяет параметры отображения модели в административной панели Django.
        """
        verbose_name = "Аналитика продаж"
        verbose_name_plural = "Аналитика продаж"
