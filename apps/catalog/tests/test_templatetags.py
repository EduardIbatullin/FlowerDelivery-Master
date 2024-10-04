# apps/catalog/tests/test_templatetags.py

from django.template import Context, Template  # Импорт классов для работы с контекстом и шаблонами в тестах
from django.test import TestCase  # Импорт базового класса TestCase для написания тестов

from apps.catalog.templatetags.catalog_filters import to_range  # Импорт пользовательского фильтра `to_range`


class CatalogTemplateTagsTest(TestCase):
    """
    Тесты для пользовательских фильтров и тегов шаблонов в приложении каталога.

    Тестируемые сценарии:
    1. Проверка корректности работы фильтра `to_range`.
    2. Проверка работы фильтра `to_range` с равными значениями.
    3. Проверка использования фильтра `to_range` в шаблоне.
    """

    def test_to_range_filter(self):
        """
        Тест фильтра `to_range` для создания диапазона.

        Проверяет, что фильтр создает корректный список чисел при передаче
        начального и конечного значения диапазона.
        """
        result = to_range(1, 5)  # Создаем диапазон от 1 до 5 включительно
        self.assertEqual(list(result), [1, 2, 3, 4, 5])  # Проверка результата: [1, 2, 3, 4, 5]

    def test_to_range_filter_with_equal_values(self):
        """
        Тест фильтра `to_range` с равными начальным и конечным значениями.

        Проверяет, что фильтр возвращает список с одним элементом, если
        начальное и конечное значение диапазона равны.
        """
        result = to_range(3, 3)  # Создаем диапазон с одним значением 3
        self.assertEqual(list(result), [3])  # Ожидаемый результат: [3]

    def test_to_range_filter_in_template(self):
        """
        Тест использования фильтра `to_range` непосредственно в шаблоне.

        Проверяет, что фильтр корректно обрабатывается в шаблоне и возвращает
        ожидаемые результаты.
        """
        # Определяем тестовый шаблон с использованием фильтра `to_range`
        template = Template('{% load catalog_filters %}{% for i in 1|to_range:3 %}{{ i }} {% endfor %}')

        # Рендерим шаблон и проверяем, что он отображает диапазон от 1 до 3
        rendered = template.render(Context({}))  # Контекст в данном случае пустой
        self.assertEqual(rendered.strip(), '1 2 3')  # Ожидаемый вывод: "1 2 3"
