# bot/keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup  # Импортируем классы для создания кнопок и клавиатур в Telegram
from config import DJANGO_SERVER_URL  # Импортируем URL сервера Django из конфигурационного файла


def get_register_button_keyboard():
    """
    Формирует клавиатуру с кнопкой регистрации в телеграм-боте.

    Возвращает:
        InlineKeyboardMarkup: Объект клавиатуры с кнопкой регистрации.
    """
    keyboard = [
        [InlineKeyboardButton(text="Зарегистрироваться в телеграм-боте", callback_data="register")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_profile_keyboard(profile_url):
    """
    Формирует клавиатуру с кнопкой для возврата в профиль пользователя.

    Аргументы:
        profile_url (str): URL профиля пользователя на сервере Django.

    Возвращает:
        InlineKeyboardMarkup: Объект клавиатуры с кнопкой возврата в профиль.
    """
    keyboard = [
        [InlineKeyboardButton(text="Вернуться в профиль", url=profile_url)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_not_admin_options_keyboard():
    """
    Формирует клавиатуру для обычных пользователей с кнопкой перехода на сайт.

    Возвращает:
        InlineKeyboardMarkup: Объект клавиатуры с кнопкой перехода на сайт.
    """
    keyboard = [
        [InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_options_keyboard():
    """
    Формирует клавиатуру для администраторов с кнопкой просмотра аналитики и перехода на сайт.

    Возвращает:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками для администраторов.
    """
    keyboard = [
        [InlineKeyboardButton(text="Посмотреть аналитику", callback_data="view_analytics")],
        [InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_analytics_period_keyboard():
    """
    Возвращает клавиатуру с кнопками для выбора периода аналитики.

    Кнопки соответствуют разным периодам (например, "Год", "Месяц" и т.д.), которые можно использовать для фильтрации данных.

    Возвращает:
        InlineKeyboardMarkup: Объект клавиатуры с кнопками периодов аналитики.
    """
    keyboard = [
        [InlineKeyboardButton(text="За все время", callback_data="За все время")],
        [InlineKeyboardButton(text="Год", callback_data="Год")],
        [InlineKeyboardButton(text="6 месяцев", callback_data="6 месяцев")],
        [InlineKeyboardButton(text="3 месяца", callback_data="3 месяца")],
        [InlineKeyboardButton(text="Месяц", callback_data="Месяц")],
        [InlineKeyboardButton(text="2 недели", callback_data="2 недели")],
        [InlineKeyboardButton(text="Неделя", callback_data="Неделя")],
        [InlineKeyboardButton(text="День", callback_data="День")]
    ]
    return InlineKeyboardMarkup(keyboard)
