# bot/keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import DJANGO_SERVER_URL


def get_register_button_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Зарегистрироваться в телеграм-боте", callback_data="register")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_profile_keyboard(profile_url):
    keyboard = [
        [InlineKeyboardButton(text="Вернуться в профиль", url=profile_url)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_not_admin_options_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_options_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="Посмотреть аналитику", callback_data="view_analytics")],
        [InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_analytics_period_keyboard():
    """
    Возвращает клавиатуру с кнопками для выбора периода аналитики.
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
