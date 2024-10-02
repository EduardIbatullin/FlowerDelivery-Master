# bot/tests/test_keyboards.py

import unittest
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.keyboards import (
    get_register_button_keyboard, get_back_to_profile_keyboard,
    get_not_admin_options_keyboard, get_admin_options_keyboard,
    get_analytics_period_keyboard
)
from config import DJANGO_SERVER_URL


class BotKeyboardsTest(unittest.TestCase):

    def test_get_register_button_keyboard(self):
        """Тест клавиатуры для регистрации в телеграм-боте."""
        keyboard = get_register_button_keyboard()
        expected_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Зарегистрироваться в телеграм-боте", callback_data="register")]]
        )
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_back_to_profile_keyboard(self):
        """Тест клавиатуры для возвращения в профиль."""
        profile_url = f"{DJANGO_SERVER_URL}/users/profile/"
        keyboard = get_back_to_profile_keyboard(profile_url)
        expected_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Вернуться в профиль", url=profile_url)]]
        )
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_not_admin_options_keyboard(self):
        """Тест клавиатуры для неадминистративных опций."""
        keyboard = get_not_admin_options_keyboard()
        expected_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]]
        )
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_admin_options_keyboard(self):
        """Тест клавиатуры для административных опций."""
        keyboard = get_admin_options_keyboard()
        expected_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Посмотреть аналитику", callback_data="view_analytics")],
                [InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]
            ]
        )
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_analytics_period_keyboard(self):
        """Тест клавиатуры для выбора периода аналитики."""
        keyboard = get_analytics_period_keyboard()
        expected_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="За все время", callback_data="За все время")],
                [InlineKeyboardButton(text="Год", callback_data="Год")],
                [InlineKeyboardButton(text="6 месяцев", callback_data="6 месяцев")],
                [InlineKeyboardButton(text="3 месяца", callback_data="3 месяца")],
                [InlineKeyboardButton(text="Месяц", callback_data="Месяц")],
                [InlineKeyboardButton(text="2 недели", callback_data="2 недели")],
                [InlineKeyboardButton(text="Неделя", callback_data="Неделя")],
                [InlineKeyboardButton(text="День", callback_data="День")]
            ]
        )
        self.assertEqual(keyboard, expected_keyboard)


if __name__ == '__main__':
    unittest.main()
