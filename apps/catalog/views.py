# apps/catalog/views.py

from django.shortcuts import render, get_object_or_404  # Импорт функций для отображения шаблонов и получения объектов из базы данных

from .models import Product  # Импорт модели Product для работы с данными продуктов
from apps.reviews.models import Review  # Импорт модели Review для работы с отзывами на продукты
from ..reviews.forms import ReviewForm  # Импорт формы ReviewForm для добавления новых отзывов


def catalog_list_view(request):
    """
    Отображает список всех продуктов в каталоге.

    Функция извлекает все продукты из базы данных и вычисляет их средний рейтинг.
    Результат передается в шаблон 'catalog/catalog_list.html' для отображения списка продуктов.

    Аргументы:
        request (HttpRequest): Объект запроса от клиента, содержащий информацию о текущем запросе.

    Возвращает:
        HttpResponse: Рендерит HTML-шаблон со списком продуктов, передавая его в контексте.
    """
    products = Product.objects.all()  # Извлечение всех продуктов из базы данных
    for product in products:
        product.average_rating = product.average_rating()  # Расчет среднего рейтинга для каждого продукта

    return render(request, 'catalog/catalog_list.html', {'products': products})  # Рендеринг шаблона со списком продуктов


def product_detail_view(request, pk):
    """
    Отображает страницу с подробной информацией о продукте.

    Функция находит продукт по его первичному ключу (pk), извлекает все связанные отзывы
    и передает данные о продукте, его рейтинге и форму для добавления нового отзыва в шаблон.

    Аргументы:
        request (HttpRequest): Объект запроса от клиента, содержащий информацию о текущем запросе.
        pk (int): Первичный ключ продукта, используемый для его поиска в базе данных.

    Возвращает:
        HttpResponse: Рендерит HTML-шаблон с детальной информацией о продукте и отзывами.
    """
    product = get_object_or_404(Product, pk=pk)  # Поиск продукта по его первичному ключу или возврат 404 ошибки
    reviews = product.reviews.all()  # Извлечение всех отзывов, связанных с продуктом
    product.average_rating = product.average_rating()  # Расчет среднего рейтинга для данного продукта

    form = ReviewForm()  # Создание экземпляра формы для добавления нового отзыва

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })  # Рендеринг шаблона с информацией о продукте и отзывами
