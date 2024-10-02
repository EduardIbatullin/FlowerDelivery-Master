# flowerdelivery/tests/test_views.py

from django.test import TestCase
from django.urls import reverse
from django.template.loader import render_to_string

class HomeViewTestCase(TestCase):
    """Тесты для проверки представления home_view"""

    def test_home_view_status_code(self):
        """Проверка статуса ответа для домашней страницы"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)  # Убедимся, что ответ успешен

    def test_home_view_template(self):
        """Проверка использования правильного шаблона"""
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')  # Проверяем использование шаблона

    def test_home_view_content(self):
        """Проверка содержимого домашней страницы"""
        response = self.client.get(reverse('home'))
        expected_content = render_to_string('home.html')  # Рендерим шаблон напрямую
        self.assertInHTML(expected_content, response.content.decode())  # Проверяем совпадение с ожидаемым содержимым
