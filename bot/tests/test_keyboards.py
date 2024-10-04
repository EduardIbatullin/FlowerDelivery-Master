# bot/tests/test_keyboards.py

import unittest  # Импорт библиотеки для создания и запуска тестов
from telegram import InlineKeyboardMarkup, InlineKeyboardButton  # Импорт классов для создания и тестирования Telegram-клавиатур

from bot.keyboards import (  # Импортируем тестируемые функции для создания клавиатур
    get_register_button_keyboard,
    get_back_to_profile_keyboard,
    get_not_admin_options_keyboard,
    get_admin_options_keyboard,
    get_analytics_period_keyboard
)
from config import DJANGO_SERVER_URL  # Импортируем URL сервера Django из конфигурационного файла


class BotKeyboardsTest(unittest.TestCase):
    """
    Тесты для проверки корректности создания клавиатур Telegram-бота.

    Тестируемые сценарии:
    1. Проверка клавиатуры регистрации в телеграм-боте.
    2. Проверка клавиатуры для возврата в профиль.
    3. Проверка клавиатуры для неадминистративных опций.
    4. Проверка клавиатуры для административных опций.
    5. Проверка клавиатуры для выбора периода аналитики.
    """

    def test_get_register_button_keyboard(self):
        """
        Тест клавиатуры для регистрации в телеграм-боте.

        Логика:
        - Проверяет, что возвращенная клавиатура совпадает с ожидаемой структурой.
        - Кнопка должна содержать текст "Зарегистрироваться в телеграм-боте" и передавать callback_data "register".
        """
        # Генерация клавиатуры через тестируемую функцию
        keyboard = get_register_button_keyboard()

        # Ожидаемая структура клавиатуры, созданная вручную для сравнения
        expected_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Зарегистрироваться в телеграм-боте", callback_data="register")]]
        )

        # Сравниваем сгенерированную клавиатуру с ожидаемой структурой
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_back_to_profile_keyboard(self):
        """
        Тест клавиатуры для возвращения в профиль.

        Логика:
        - Проверяет, что возвращенная клавиатура содержит кнопку "Вернуться в профиль" с ссылкой на профиль пользователя.
        """
        # Ссылка на профиль пользователя
        profile_url = f"{DJANGO_SERVER_URL}/users/profile/"

        # Генерация клавиатуры через тестируемую функцию
        keyboard = get_back_to_profile_keyboard(profile_url)

        # Ожидаемая структура клавиатуры, созданная вручную для сравнения
        expected_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Вернуться в профиль", url=profile_url)]]
        )

        # Сравниваем сгенерированную клавиатуру с ожидаемой структурой
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_not_admin_options_keyboard(self):
        """
        Тест клавиатуры для неадминистративных опций.

        Логика:
        - Проверяет, что возвращенная клавиатура содержит кнопку "Перейти на сайт" с ссылкой на сайт магазина.
        """
        # Генерация клавиатуры через тестируемую функцию
        keyboard = get_not_admin_options_keyboard()

        # Ожидаемая структура клавиатуры, созданная вручную для сравнения
        expected_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]]
        )

        # Сравниваем сгенерированную клавиатуру с ожидаемой структурой
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_admin_options_keyboard(self):
        """
        Тест клавиатуры для административных опций.

        Логика:
        - Проверяет, что клавиатура содержит кнопки для просмотра аналитики и перехода на сайт.
        - Первая кнопка должна передавать callback_data "view_analytics".
        - Вторая кнопка должна содержать ссылку на сайт магазина.
        """
        # Генерация клавиатуры через тестируемую функцию
        keyboard = get_admin_options_keyboard()

        # Ожидаемая структура клавиатуры, созданная вручную для сравнения
        expected_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Посмотреть аналитику", callback_data="view_analytics")],
                [InlineKeyboardButton(text="Перейти на сайт", url=f"{DJANGO_SERVER_URL}")]
            ]
        )

        # Сравниваем сгенерированную клавиатуру с ожидаемой структурой
        self.assertEqual(keyboard, expected_keyboard)

    def test_get_analytics_period_keyboard(self):
        """
        Тест клавиатуры для выбора периода аналитики.

        Логика:
        - Проверяет, что клавиатура содержит кнопки для всех предусмотренных периодов:
          "За все время", "Год", "6 месяцев", "3 месяца", "Месяц", "2 недели", "Неделя", "День".
        - Каждая кнопка должна передавать соответствующее значение в callback_data.
        """
        # Генерация клавиатуры через тестируемую функцию
        keyboard = get_analytics_period_keyboard()

        # Ожидаемая структура клавиатуры, созданная вручную для сравнения
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

        # Сравниваем сгенерированную клавиатуру с ожидаемой структурой
        self.assertEqual(keyboard, expected_keyboard)


if __name__ == '__main__':
    unittest.main()
