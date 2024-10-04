# flowerdelivery/views.py

from django.shortcuts import render  # Импорт функции для рендеринга HTML-страницы


def home_view(request):
    """
    Представление для главной страницы.

    Эта функция обрабатывает запросы на главную страницу сайта.
    Она использует функцию render для отображения шаблона home.html.

    Аргументы:
        request: объект запроса, содержащий данные о HTTP-запросе.

    Возвращает:
        HttpResponse: готовую HTML-страницу, сгенерированную из шаблона home.html.
    """
    return render(request, 'home.html')  # Возвращает сгенерированную страницу главной страницы
