# flowerdelivery/tests/test_views.py

from django.test import TestCase  # Импорт базового класса для тестирования представлений
from django.urls import reverse  # Импорт функции reverse для создания URL по имени маршрута
from django.template.loader import render_to_string  # Импорт функции для рендеринга шаблона в строку


class HomeViewTestCase(TestCase):
    """
    Тестовый класс для проверки представления home_view.

    Содержит тесты для проверки статуса ответа, правильного использования шаблона и
    содержимого домашней страницы, что гарантирует корректную работу основного представления.
    """

    def test_home_view_status_code(self):
        """
        Проверка статуса ответа для домашней страницы.

        Убеждается, что запрос к главной странице ('/') возвращает статус 200 (успешный ответ).
        """
        response = self.client.get(reverse('home'))  # Отправляем GET-запрос к главной странице
        self.assertEqual(response.status_code, 200)  # Проверяем, что статус ответа 200

    def test_home_view_template(self):
        """
        Проверка использования правильного шаблона.

        Убеждается, что представление home_view использует шаблон 'home.html'.
        """
        response = self.client.get(reverse('home'))  # Отправляем GET-запрос к главной странице
        self.assertTemplateUsed(response, 'home.html')  # Проверяем, что используется шаблон home.html

    def test_home_view_content(self):
        """
        Проверка содержимого домашней страницы.

        Убеждается, что содержимое главной страницы соответствует ожидаемому шаблону 'home.html'.
        """
        response = self.client.get(reverse('home'))  # Отправляем GET-запрос к главной странице
        expected_content = render_to_string('home.html')  # Рендерим шаблон 'home.html' в строку
        self.assertInHTML(expected_content, response.content.decode())  # Проверяем, что контент страницы содержит ожидаемое содержимое
