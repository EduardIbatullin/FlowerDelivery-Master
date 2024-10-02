# apps/users/permissions.py

def is_employee(user):
    """Проверка, является ли пользователь сотрудником."""
    return user.groups.filter(name='Сотрудники').exists()


def is_admin(user):
    """Проверка, является ли пользователь администратором."""
    return user.groups.filter(name='Администраторы').exists() or user.is_superuser
