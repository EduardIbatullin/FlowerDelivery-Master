from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from apps.catalog.models import Product


def review_list_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'reviews/review_list.html', {'product': product, 'reviews': reviews})


def review_create_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('review_list', product_id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_create.html', {'form': form, 'product': product})
