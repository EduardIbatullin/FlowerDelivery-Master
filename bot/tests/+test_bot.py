# bot/tests/test_bot.py

import unittest
from unittest.mock import patch, MagicMock
from bot.bot import main
from telegram.ext import CommandHandler, CallbackQueryHandler


class BotMainTestCase(unittest.TestCase):
    @patch('bot.bot.Application.builder')
    def test_bot_initialization(self, mock_builder):
        """Проверка инициализации бота и добавления хендлеров."""
        # Мок для Application
        mock_application = MagicMock()
        mock_builder.return_value.token.return_value.build.return_value = mock_application

        # Вызываем main(), чтобы проверить добавление хендлеров
        main()

        # Проверяем, что Application.builder().token().build() был вызван
        mock_builder.assert_called_once()

        # Список всех вызовов метода add_handler
        handler_calls = mock_application.add_handler.call_args_list

        # Выводим все вызовы для анализа
        print("Добавленные обработчики:", handler_calls)

        # Проверяем, что хендлеры были добавлены в приложение
        self.assertEqual(len(handler_calls), 5)  # Изменяем ожидаемое количество на 5

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

        # Проверяем, что бот запускается с run_polling
        mock_application.run_polling.assert_called_once()


if __name__ == '__main__':
    unittest.main()
