# apps/catalog/templatetags/catalog_filters.py

from django import template

register = template.Library()


@register.filter
def to_range(start, end):
    """
    Преобразует два значения в диапазон. Например, {% for i in 1|to_range:5 %} создаст диапазон [1, 2, 3, 4, 5].
    """
    return range(start, end + 1)
