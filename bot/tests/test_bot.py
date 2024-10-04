# bot/tests/test_bot.py

import unittest  # Импорт библиотеки для создания и запуска тестов
from unittest.mock import patch, MagicMock  # Импорт инструментов для создания мок-объектов и подмены реальных зависимостей
from telegram.ext import CommandHandler, CallbackQueryHandler  # Импорт классов для обработки команд и запросов в Telegram

from bot.bot import main  # Импорт основной функции запуска бота для тестирования


class BotMainTestCase(unittest.TestCase):
    """
    Тесты для проверки инициализации бота и добавления хендлеров.

    Тестируемые сценарии:
    1. Проверка инициализации и конфигурации бота.
    2. Проверка добавления всех необходимых хендлеров (CommandHandler и CallbackQueryHandler).
    3. Проверка корректного запуска бота с помощью run_polling.
    """

    @patch('bot.bot.Application.builder')
    def test_bot_initialization(self, mock_builder):
        """
        Проверка инициализации бота и добавления всех хендлеров.

        Логика:
        - Использует мок-объекты для подмены методов создания и инициализации бота.
        - Проверяет, что все хендлеры (обработчики команд и запросов) были добавлены в приложение.
        - Проверяет корректность вызова метода run_polling для запуска бота.
        """
        # Создаем мок-объект Application и подменяем метод builder
        mock_application = MagicMock()
        mock_builder.return_value.token.return_value.build.return_value = mock_application

        # Вызываем main(), чтобы проверить добавление хендлеров
        main()

        # Проверяем, что Application.builder().token().build() был вызван для создания приложения
        mock_builder.assert_called_once()

        # Список всех вызовов метода add_handler, чтобы проверить, какие хендлеры были добавлены
        handler_calls = mock_application.add_handler.call_args_list

        # Проверка количества добавленных обработчиков (всего 5)
        self.assertEqual(len(handler_calls), 5)

        # Проверяем, что были добавлены два CommandHandler для команды "start"
        start_handlers = [call for call in handler_calls if isinstance(call[0][0], CommandHandler)]
        self.assertEqual(len(start_handlers), 2)

        # Проверяем, что CallbackQueryHandler для регистрации был добавлен
        register_handler_calls = [call for call in handler_calls if isinstance(call[0][0], CallbackQueryHandler) and call[0][0].callback.__name__ == 'register_callback']
        self.assertEqual(len(register_handler_calls), 1)

        # Проверяем, что CallbackQueryHandler для просмотра аналитики был добавлен
        analytics_handler_calls = [call for call in handler_calls if isinstance(call[0][0], CallbackQueryHandler) and call[0][0].callback.__name__ == 'view_analytics_handler']
        self.assertEqual(len(analytics_handler_calls), 1)

        # Проверяем, что CallbackQueryHandler для аналитики был добавлен
        other_handler_calls = [call for call in handler_calls if isinstance(call[0][0], CallbackQueryHandler) and call[0][0].callback.__name__ == 'analytics_handler']
        self.assertEqual(len(other_handler_calls), 1)

        # Проверяем, что бот запускается с run_polling, что свидетельствует о корректной инициализации
        mock_application.run_polling.assert_called_once()


if __name__ == '__main__':
    unittest.main()
