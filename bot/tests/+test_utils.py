# bot/tests/test_utils.py

import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from bot.utils import (
    send_telegram_message, send_post_request, get_sales_analytics, generate_sales_chart,
    aggregate_sales_data, format_date, get_dates_by_period
)
from datetime import datetime, timedelta
from io import BytesIO
import matplotlib.pyplot as plt


class BotUtilsTest(unittest.IsolatedAsyncioTestCase):

    @patch('bot.utils.aiohttp.ClientSession')
    @patch('bot.utils.TELEGRAM_API_URL', 'https://api.telegram.org/botTEST_TOKEN/sendMessage')
    async def test_send_telegram_message(self, mock_session):
        """Тест отправки сообщения в Telegram."""
        # Создаем асинхронный мок для session.post
        mock_post = MagicMock()
        mock_response = AsyncMock()
        mock_response.status = 200

        # Настройка асинхронного контекстного менеджера
        mock_response.__aenter__.return_value = mock_response
        mock_post.return_value = mock_response

        # Поддержка асинхронного контекста
        mock_session.return_value.__aenter__.return_value = mock_session.return_value
        mock_session.return_value.post = mock_post

        chat_id = 123456
        text = "Test message"

        # Тест успешной отправки
        await send_telegram_message(chat_id, text)
        mock_post.assert_called_once_with(
            'https://api.telegram.org/botTEST_TOKEN/sendMessage',
            json={"chat_id": chat_id, "text": text},
            timeout=10
        )

        # Тест неудачной отправки
        mock_response.status = 400
        with self.assertRaises(Exception):
            await send_telegram_message(chat_id, text)

    @patch('bot.utils.aiohttp.ClientSession')
    async def test_send_post_request(self, mock_session):
        """Тест отправки POST-запроса на сервер Django."""
        # Создаем асинхронный мок для session.post
        mock_post = MagicMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={'status': 'success'})

        # Настройка асинхронного контекстного менеджера
        mock_response.__aenter__.return_value = mock_response
        mock_post.return_value = mock_response

        # Поддержка асинхронного контекста
        mock_session.return_value.__aenter__.return_value = mock_session.return_value
        mock_session.return_value.post = mock_post

        endpoint = 'test_endpoint'
        data = {'key': 'value'}

        # Выполнение тестируемой функции
        response = await send_post_request(endpoint, data)
        self.assertEqual(response, {'status': 'success'})

        # Проверка отправки запроса с правильными параметрами
        mock_post.assert_called_once_with(
            f'http://127.0.0.1:8000/{endpoint}/',
            json=data,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            timeout=10
        )

    @patch('bot.utils.send_post_request', new_callable=AsyncMock)
    async def test_get_sales_analytics(self, mock_send_post_request):
        """Тест получения данных аналитики."""
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        telegram_id = 123456

        mock_send_post_request.return_value = {'status': 'success', 'data': []}
        response = await get_sales_analytics(start_date, end_date, telegram_id)

        mock_send_post_request.assert_called_once_with(
            'analytics/get_analytics_data',
            {'period_start': start_date, 'period_end': end_date, 'telegram_id': telegram_id, 'product_id': None}
        )
        self.assertEqual(response, {'status': 'success', 'data': []})

    def test_generate_sales_chart(self):
        """Тест генерации графика аналитики продаж."""
        analytics_data = {
            'data': [
                {'period_start': '2023-09-01', 'total_sales': 5, 'total_revenue': 1000},
                {'period_start': '2023-09-02', 'total_sales': 3, 'total_revenue': 500}
            ]
        }
        buffer = generate_sales_chart(analytics_data)

        # Проверка, что результат является экземпляром BytesIO
        self.assertIsInstance(buffer, BytesIO)

        # Проверка, что данные могут быть прочитаны как изображение
        plt.imread(buffer)  # Если не является изображением, вызовет исключение

    def test_aggregate_sales_data(self):
        """Тест агрегации данных аналитики."""
        data = [
            {'period_start': '2023-09-01', 'total_sales': 5, 'total_revenue': 1000},
            {'period_start': '2023-09-01', 'total_sales': 3, 'total_revenue': 500},
            {'period_start': '2023-09-02', 'total_sales': 2, 'total_revenue': 300}
        ]
        expected_result = [
            {'period_start': '2023-09-01', 'total_sales': 8, 'total_revenue': 1500},
            {'period_start': '2023-09-02', 'total_sales': 2, 'total_revenue': 300}
        ]

        result = aggregate_sales_data(data)
        self.assertEqual(result, expected_result)

    def test_format_date(self):
        """Тест форматирования даты."""
        date_str = '2023-09-01'
        expected_result = '01.09.2023'
        result = format_date(date_str)
        self.assertEqual(result, expected_result)

    def test_get_dates_by_period(self):
        """Тест получения дат по периоду."""
        period = "Месяц"
        start_date, end_date = get_dates_by_period(period)

        expected_start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        expected_end_date = datetime.today().strftime("%Y-%m-%d")

        self.assertEqual(start_date, expected_start_date)
        self.assertEqual(end_date, expected_end_date)


if __name__ == '__main__':
    unittest.main()
