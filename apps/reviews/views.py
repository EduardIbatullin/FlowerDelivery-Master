# apps/reviews/views.py

from django.shortcuts import render, get_object_or_404, redirect
from apps.catalog.models import Product
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Ваш отзыв добавлен.")
            return redirect('catalog:product_detail', pk=product.id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/add_review.html', {'form': form, 'product': product})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product = review.product

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Ваш отзыв был успешно обновлен.")
            return redirect('catalog:product_detail', pk=product.id)
    else:
        form = ReviewForm(instance=review)  # Предзаполняем форму данными

    reviews = product.reviews.all()
    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'edit_review_id': review.id,  # Передаем ID редактируемого отзыва
    }

    # Рендерим страницу с отзывами и предзаполненной формой редактирования
    return render(request, 'catalog/product_detail.html', context)
