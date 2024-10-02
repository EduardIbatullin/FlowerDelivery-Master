# apps/users/templatetags/custom_filters.py

from django import template
from apps.users.permissions import is_admin, is_employee

register = template.Library()


@register.filter(name='is_admin')
def check_is_admin(user):
    return is_admin(user)


@register.filter(name='is_employee')
def check_is_employee(user):
    return is_employee(user)
