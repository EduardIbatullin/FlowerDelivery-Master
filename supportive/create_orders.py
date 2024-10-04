# create_orders.py

# -*- coding: utf-8 -*-
import sys
import locale
import random
from django.utils import timezone
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product
from datetime import datetime, timedelta

# Установить правильную кодировку для stdout и stderr
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


# Задаем начальные параметры
start_date = datetime(2024, 6, 1)  # Начало периода (1 июня 2024)
user_ids = [2, 3]  # ID существующих пользователей
products = Product.objects.all()  # Все доступные продукты в каталоге

# Убедитесь, что в базе данных есть товары
if not products.exists():
    print("В базе данных нет товаров. Добавьте товары перед выполнением скрипта.")
else:
    # Перебираем 100 заказов
    for i in range(100):
        # Случайный пользователь
        user_id = random.choice(user_ids)

        # Вычисляем дату создания и доставки (каждый следующий заказ на 1-2 дня позже)
        created_at = start_date + timedelta(days=i)
        delivery_date = created_at + timedelta(days=random.randint(1, 2))  # Доставка на 1-2 дня позже

        # Создаем заказ
        order = Order.objects.create(
            user_id=user_id,
            status='Доставлен',
            delivery_address=f'Адрес доставки {i + 1}',
            contact_phone=f'8{random.randint(1000000000, 9999999999)}',
            delivery_date=delivery_date,
            delivery_time=timezone.now().time(),
            email_notifications=True,
            telegram_notifications=True,
            total_price=0,  # Будет вычислено позже
            complete=True
        )

        total_price = 0

        # Добавляем случайное количество товаров в заказ (от 1 до 3 позиций)
        for _ in range(random.randint(1, 3)):
            product = random.choice(products)
            quantity = random.randint(1, 5)  # Количество от 1 до 5
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=product.price
            )
            # Обновляем общую стоимость заказа
            total_price += product.price * quantity

        # Обновляем общую стоимость заказа
        order.total_price = total_price
        order.save()

    print("100 заказов успешно созданы.")
