# apps/reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect  # Утилиты для обработки запросов и формирования ответов
from django.contrib.auth.decorators import login_required  # Декоратор для ограничения доступа неавторизованным пользователям
from django.contrib import messages  # Фреймворк для отправки уведомлений пользователям

from apps.catalog.models import Product  # Импорт модели продукта из приложения каталога
from .models import Review  # Импорт модели отзыва из текущего приложения
from .forms import ReviewForm  # Импорт формы для создания и редактирования отзывов


@login_required
def add_review(request, product_id):
    """
    Позволяет авторизованному пользователю добавить отзыв к выбранному продукту.

    Обрабатывает GET и POST запросы для создания нового отзыва. Если метод запроса POST, то данные формы проверяются и
    сохраняются. В противном случае отображается пустая форма для заполнения.

    Аргументы:
        request: Объект HttpRequest с данными запроса пользователя.
        product_id: Идентификатор продукта, к которому добавляется отзыв.

    Возвращает:
        HttpResponse: Перенаправляет на страницу детали продукта после успешного добавления отзыва или отображает
        страницу с формой добавления отзыва.
    """
    product = get_object_or_404(Product, pk=product_id)  # Получаем продукт по идентификатору или возвращаем 404
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Устанавливаем текущего пользователя как автора отзыва
            review.product = product  # Привязываем отзыв к продукту
            review.save()  # Сохраняем отзыв в базе данных
            messages.success(request, "Ваш отзыв добавлен.")  # Отправляем сообщение об успешном добавлении
            return redirect('catalog:product_detail', pk=product.id)  # Перенаправляем на страницу продукта
    else:
        form = ReviewForm()  # Инициализируем пустую форму для нового отзыва

    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})  # Отображаем страницу добавления отзыва


@login_required
def edit_review(request, review_id):
    """
    Позволяет авторизованному пользователю редактировать свой существующий отзыв.

    Обрабатывает GET и POST запросы для редактирования отзыва. Если метод запроса POST, то данные формы проверяются и
    обновляются. В противном случае отображается форма с предзаполненными данными отзыва.

    Аргументы:
        request: Объект HttpRequest с данными запроса пользователя.
        review_id: Идентификатор отзыва, который требуется отредактировать.

    Возвращает:
        HttpResponse: Перенаправляет на страницу детали продукта после успешного обновления отзыва или отображает
        страницу с формой редактирования отзыва.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)  # Получаем отзыв текущего пользователя или 404
    product = review.product  # Получаем связанный продукт

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()  # Сохраняем изменения отзыва
            messages.success(request, "Ваш отзыв был успешно обновлен.")  # Отправляем сообщение об успешном обновлении
            return redirect('catalog:product_detail', pk=product.id)  # Перенаправляем на страницу продукта
    else:
        form = ReviewForm(instance=review)  # Предзаполняем форму данными существующего отзыва

    reviews = product.reviews.all()  # Получаем все отзывы к продукту
    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'edit_review_id': review.id,  # Передаем ID редактируемого отзыва для идентификации на странице
    }

    return render(request, 'catalog/product_detail.html', context)  # Отображаем страницу продукта с формой редактирования
