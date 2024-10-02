# apps/catalog/tests/test_templatetags.py

from django.test import TestCase
from django.template import Context, Template
from apps.catalog.templatetags.catalog_filters import to_range


class CatalogTemplateTagsTest(TestCase):

    def test_to_range_filter(self):
        """Тест фильтра to_range для создания диапазона."""
        result = to_range(1, 5)
        self.assertEqual(list(result), [1, 2, 3, 4, 5])

    def test_to_range_filter_with_equal_values(self):
        """Тест фильтра to_range с равными начальным и конечным значениями."""
        result = to_range(3, 3)
        self.assertEqual(list(result), [3])

    def test_to_range_filter_in_template(self):
        """Тест использования фильтра to_range непосредственно в шаблоне."""
        template = Template('{% load catalog_filters %}{% for i in 1|to_range:3 %}{{ i }} {% endfor %}')
        rendered = template.render(Context({}))
        self.assertEqual(rendered.strip(), '1 2 3')
