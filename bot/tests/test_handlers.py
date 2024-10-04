# bot/tests/test_handlers.py

import unittest  # Импорт библиотеки для создания и запуска тестов
from unittest.mock import patch, AsyncMock, MagicMock  # Импорт инструментов для создания мок-объектов и подмены реальных зависимостей
from telegram import Update, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile  # Импорт классов для работы с Telegram API
from telegram.ext import ContextTypes  # Импорт контекстного типа для асинхронных вызовов бота

from bot.handlers import (  # Импортируем обработчики событий для тестирования
    register_start_command,
    register_callback,
    handle_start_command,
    view_analytics_handler,
    analytics_handler,
    send_sales_chart
)


class BotHandlersTest(unittest.IsolatedAsyncioTestCase):
    """
    Тесты для проверки работы основных хендлеров (обработчиков) в боте.

    Тестируемые сценарии:
    1. Проверка корректной работы команды /start с параметром user_id.
    2. Проверка корректной работы команды /start без параметров (вызов напрямую из бота).
    3. Проверка обработки нажатия на кнопку регистрации.
    4. Проверка обработки нажатия на кнопку аналитики.
    5. Проверка отправки графика продаж.
    """

    @patch('bot.handlers.send_post_request', new_callable=AsyncMock)
    async def test_register_start_command(self, mock_send_post_request):
        """
        Тест команды /start с параметром user_id.

        Логика:
        - Мокаем аргументы команды /start (передаем user_id).
        - Мокаем успешный ответ сервера Django с данными пользователя.
        - Проверяем, что отправленное сообщение содержит корректный текст и клавиатуру с кнопкой регистрации.
        """
        mock_update = MagicMock(Update)
        mock_context = MagicMock(ContextTypes.DEFAULT_TYPE)
        mock_context.args = ['1']  # Передаем user_id как аргумент команды /start
        mock_update.message.reply_text = AsyncMock()

        # Мокаем успешный ответ сервера Django
        mock_send_post_request.return_value = {
            'status': 'success',
            'first_name': 'TestUser'
        }

        # Вызываем тестируемый метод
        await register_start_command(mock_update, mock_context)

        # Проверяем, что сообщение было отправлено с ожидаемым текстом и клавиатурой
        mock_update.message.reply_text.assert_called_once_with(
            'Мы рады приветствовать вас TestUser. Для сохранения Вашего Telegram ID, пожалуйста, нажмите кнопку ниже.',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Зарегистрироваться в телеграм-боте", callback_data="register")]])
        )

    @patch('bot.handlers.send_post_request', new_callable=AsyncMock)
    async def test_register_callback(self, mock_send_post_request):
        """
        Тест обработки нажатия на кнопку регистрации.

        Логика:
        - Мокаем CallbackQuery и user_id в контексте.
        - Мокаем успешный ответ сервера Django.
        - Проверяем, что отправленное сообщение содержит подтверждение успешной регистрации и кнопку перехода в профиль.
        """
        mock_update = MagicMock(Update)
        mock_context = MagicMock(ContextTypes.DEFAULT_TYPE)

        # Мокаем CallbackQuery и user_id
        mock_query = MagicMock(CallbackQuery)
        mock_query.answer = AsyncMock()
        mock_update.callback_query = mock_query
        mock_query.edit_message_text = AsyncMock()
        mock_context.user_data = {'user_id': '1'}
        mock_send_post_request.return_value = {'status': 'success'}

        # Вызываем тестируемый метод
        await register_callback(mock_update, mock_context)

        # Проверяем, что сообщение было отправлено с ожидаемым текстом и клавиатурой
        mock_query.edit_message_text.assert_called_once_with(
            text='Telegram ID успешно сохранен. Вы можете вернуться в свой профиль на сайте магазина.',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Вернуться в профиль", url="http://127.0.0.1:8000/users/profile/")]])
        )

    @patch('bot.handlers.send_post_request', new_callable=AsyncMock)
    async def test_handle_start_command(self, mock_send_post_request):
        """
        Тест команды /start, вызываемой напрямую из бота.

        Логика:
        - Мокаем запрос на сервер и успешный ответ.
        - Проверяем, что при отсутствии параметров отправляется приветственное сообщение с кнопкой перехода на сайт.
        """
        mock_update = MagicMock(Update)
        mock_context = MagicMock(ContextTypes.DEFAULT_TYPE)
        mock_update.message.reply_text = AsyncMock()

        # Мокаем успешный ответ сервера Django
        mock_send_post_request.return_value = {'status': 'success', 'user_data': {'is_admin': False}}

        # Вызываем тестируемый метод
        await handle_start_command(mock_update, mock_context)

        # Проверяем, что сообщение было отправлено с ожидаемым текстом и клавиатурой
        mock_update.message.reply_text.assert_called_once_with(
            'Мы рады приветствовать вас в нашем цветочном магазине "Classic Floral Shop"! 🌸\nВ нашем магазине вы найдете цветы на любой вкус и повод. Мы стремимся делать ваш мир ярче, доставляя радость и красоту с каждым букетом.',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Перейти на сайт", url="http://127.0.0.1:8000")]])
        )

    @patch('bot.handlers.send_sales_chart')
    @patch('bot.handlers.get_sales_analytics', new_callable=AsyncMock)
    async def test_analytics_handler(self, mock_get_sales_analytics, mock_send_sales_chart):
        """
        Тест обработки нажатия на кнопку аналитики.

        Логика:
        - Мокаем ответ сервера с аналитическими данными.
        - Проверяем, что отправлено сообщение с данными аналитики.
        - Проверяем, что отправка графика была вызвана.
        """
        mock_update = MagicMock(Update)
        mock_context = MagicMock(ContextTypes.DEFAULT_TYPE)

        # Мокаем CallbackQuery и необходимые методы
        mock_query = MagicMock(CallbackQuery)
        mock_query.answer = AsyncMock()
        mock_query.edit_message_text = AsyncMock()
        mock_context.bot.send_message = AsyncMock()  # Используем AsyncMock для асинхронных вызовов
        mock_update.callback_query = mock_query

        # Устанавливаем значение для query.data, чтобы избежать вывода мок-объекта
        mock_query.data = 'За месяц'

        # Мокаем успешный ответ с аналитическими данными
        mock_get_sales_analytics.return_value = {'status': 'success', 'total_orders': 5, 'total_revenue': 10000}

        # Вызываем тестируемый метод
        await analytics_handler(mock_update, mock_context)

        # Проверяем, что сообщение с аналитикой было отправлено
        mock_query.edit_message_text.assert_called_once_with(
            text="Аналитика за выбранный период (За месяц):\n\nОбщее количество заказов: 5 заказов\nОбщая выручка: 10000 руб.\n\n"
        )
        mock_send_sales_chart.assert_called_once()

    @patch('bot.handlers.generate_sales_chart')
    async def test_send_sales_chart(self, mock_generate_sales_chart):
        """
        Тест отправки графика продаж.

        Логика:
        - Мокаем создание изображения графика.
        - Проверяем, что изображение было отправлено в сообщении Telegram.
        """
        mock_update = MagicMock(Update)
        mock_context = MagicMock(ContextTypes.DEFAULT_TYPE)

        # Мокаем CallbackQuery и создание файла графика
        mock_query = MagicMock(CallbackQuery)
        mock_update.callback_query = mock_query
        mock_buffer = MagicMock()
        mock_generate_sales_chart.return_value = mock_buffer

        mock_query.message.reply_photo = AsyncMock()  # Используем AsyncMock для асинхронного вызова

        # Вызываем тестируемый метод
        await send_sales_chart(mock_update, mock_context, {'status': 'success'})

        # Проверяем, что изображение было отправлено
        mock_query.message.reply_photo.assert_called_once()
        args, kwargs = mock_query.message.reply_photo.call_args
        self.assertIsInstance(kwargs['photo'], InputFile)
        self.assertEqual(kwargs['photo'].filename, 'sales_chart.png')
        self.assertEqual(kwargs['caption'], 'График продаж за выбранный период.')
        mock_buffer.close.assert_called_once()  # Проверяем, что буфер был закрыт после использования


if __name__ == '__main__':
    unittest.main()
