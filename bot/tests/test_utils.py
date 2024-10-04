# bot/tests/test_utils.py

from datetime import datetime, timedelta  # Импортируем классы для работы с датами
from io import BytesIO  # Импортируем класс для работы с бинарными данными
import matplotlib.pyplot as plt  # Импортируем библиотеку для создания графиков
import unittest  # Импортируем модуль для создания и выполнения тестов
from unittest.mock import patch, AsyncMock, MagicMock  # Импортируем необходимые классы для создания моков и патчей

from bot.utils import (  # Импортируем тестируемые функции из модуля bot.utils
    send_telegram_message, send_post_request, get_sales_analytics, generate_sales_chart,
    aggregate_sales_data, format_date, get_dates_by_period
)


class BotUtilsTest(unittest.IsolatedAsyncioTestCase):
    """
    Тесты для проверки утилитных функций, используемых в боте.

    Тестируемые сценарии:
    1. Отправка сообщения в Telegram.
    2. Отправка POST-запроса на сервер Django.
    3. Получение данных аналитики.
    4. Генерация графика аналитики продаж.
    5. Агрегация данных аналитики.
    6. Форматирование даты.
    7. Получение дат по заданному периоду.
    """

    @patch('bot.utils.aiohttp.ClientSession')
    @patch('bot.utils.TELEGRAM_API_URL', 'https://api.telegram.org/botTEST_TOKEN/sendMessage')
    async def test_send_telegram_message(self, mock_session):
        """
        Тест отправки сообщения в Telegram.

        Логика:
        - Проверяет, что запрос отправки сообщения в Telegram API выполняется корректно.
        - При успешной отправке, ответ имеет статус 200.
        - При ошибке отправки должен выбрасываться соответствующий Exception.
        """
        # Создаем асинхронный мок для session.post
        mock_post = MagicMock()
        mock_response = AsyncMock()
        mock_response.status = 200  # Успешный статус ответа

        # Настройка асинхронного контекстного менеджера для session.post
        mock_response.__aenter__.return_value = mock_response
        mock_post.return_value = mock_response
        mock_session.return_value.__aenter__.return_value = mock_session.return_value
        mock_session.return_value.post = mock_post

        # Параметры отправки сообщения
        chat_id = 123456
        text = "Test message"

        # Тест успешной отправки сообщения
        await send_telegram_message(chat_id, text)
        # Проверяем, что вызов был отправлен с корректными параметрами
        mock_post.assert_called_once_with(
            'https://api.telegram.org/botTEST_TOKEN/sendMessage',
            json={"chat_id": chat_id, "text": text},
            timeout=10
        )

        # Тест неудачной отправки (изменяем статус на 400)
        mock_response.status = 400
        # Ожидаем, что вызов функции при статусе 400 вызовет исключение
        with self.assertRaises(Exception):
            await send_telegram_message(chat_id, text)

    @patch('bot.utils.aiohttp.ClientSession')
    async def test_send_post_request(self, mock_session):
        """
        Тест отправки POST-запроса на сервер Django.

        Логика:
        - Проверяет корректность выполнения POST-запроса на сервер.
        - Убедиться, что запрос отправляется с правильными параметрами.
        - Проверяет, что при успешном ответе возвращается корректное значение.
        """
        # Создаем асинхронный мок для session.post
        mock_post = MagicMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={'status': 'success'})

        # Настройка асинхронного контекстного менеджера для session.post
        mock_response.__aenter__.return_value = mock_response
        mock_post.return_value = mock_response
        mock_session.return_value.__aenter__.return_value = mock_session.return_value
        mock_session.return_value.post = mock_post

        # Параметры для отправки POST-запроса
        endpoint = 'test_endpoint'
        data = {'key': 'value'}

        # Выполнение тестируемой функции
        response = await send_post_request(endpoint, data)
        # Проверяем, что функция возвращает ожидаемое значение
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
        """
        Тест получения данных аналитики с сервера.

        Логика:
        - Отправляет запрос на получение аналитики за заданный период.
        - Проверяет, что запрос отправляется с корректными параметрами (период, telegram_id).
        - Проверяет, что ответ содержит ожидаемые данные.
        """
        # Инициализация параметров для теста
        start_date = "2023-01-01"
        end_date = "2023-12-31"
        telegram_id = 123456

        # Мокаем успешный ответ от сервера
        mock_send_post_request.return_value = {'status': 'success', 'data': []}

        # Выполнение тестируемой функции
        response = await get_sales_analytics(start_date, end_date, telegram_id)

        # Проверка, что функция отправила запрос с правильными параметрами
        mock_send_post_request.assert_called_once_with(
            'analytics/get_analytics_data',
            {'period_start': start_date, 'period_end': end_date, 'telegram_id': telegram_id, 'product_id': None}
        )
        # Проверка, что возвращенные данные соответствуют ожидаемым
        self.assertEqual(response, {'status': 'success', 'data': []})

    def test_generate_sales_chart(self):
        """
        Тест генерации графика аналитики продаж.

        Логика:
        - Генерирует график продаж на основе данных.
        - Проверяет, что результат является изображением (BytesIO).
        - Убеждается, что изображение может быть корректно прочитано с помощью plt.imread.
        """
        # Инициализация данных для теста
        analytics_data = {
            'data': [
                {'period_start': '2023-09-01', 'total_sales': 5, 'total_revenue': 1000},
                {'period_start': '2023-09-02', 'total_sales': 3, 'total_revenue': 500}
            ]
        }

        # Генерация графика
        buffer = generate_sales_chart(analytics_data)

        # Проверка, что результат является экземпляром BytesIO (проверка формата данных)
        self.assertIsInstance(buffer, BytesIO)

        # Проверка, что данные могут быть прочитаны как изображение
        plt.imread(buffer)  # Если не является изображением, вызовет исключение

    def test_aggregate_sales_data(self):
        """
        Тест агрегации данных аналитики.

        Логика:
        - Проверяет, что данные корректно суммируются по каждому периоду.
        - Убеждается, что при совпадении дат значения полей total_sales и total_revenue складываются.
        """
        # Инициализация тестовых данных
        data = [
            {'period_start': '2023-09-01', 'total_sales': 5, 'total_revenue': 1000},
            {'period_start': '2023-09-01', 'total_sales': 3, 'total_revenue': 500},
            {'period_start': '2023-09-02', 'total_sales': 2, 'total_revenue': 300}
        ]

        # Ожидаемый результат агрегации данных
        expected_result = [
            {'period_start': '2023-09-01', 'total_sales': 8, 'total_revenue': 1500},
            {'period_start': '2023-09-02', 'total_sales': 2, 'total_revenue': 300}
        ]

        # Выполнение функции агрегации
        result = aggregate_sales_data(data)
        # Проверка, что результат соответствует ожиданиям
        self.assertEqual(result, expected_result)

    def test_format_date(self):
        """
        Тест форматирования даты.

        Логика:
        - Проверяет преобразование даты из формата YYYY-MM-DD в DD.MM.YYYY.
        """
        date_str = '2023-09-01'
        expected_result = '01.09.2023'
        result = format_date(date_str)
        self.assertEqual(result, expected_result)

    def test_get_dates_by_period(self):
        """
        Тест получения дат по заданному периоду.

        Логика:
        - Проверяет, что начало и конец периода корректно рассчитываются.
        - Например, для периода "Месяц" начальная дата должна быть 30 дней назад от сегодняшнего дня.
        """
        # Задаем тестируемый период
        period = "Месяц"
        start_date, end_date = get_dates_by_period(period)

        # Ожидаемые даты для тестируемого периода
        expected_start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
        expected_end_date = datetime.today().strftime("%Y-%m-%d")

        # Проверка, что начальная и конечная даты совпадают с ожидаемыми
        self.assertEqual(start_date, expected_start_date)
        self.assertEqual(end_date, expected_end_date)


if __name__ == '__main__':
    unittest.main()
