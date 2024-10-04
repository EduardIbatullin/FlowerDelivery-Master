# FlowerDelivery-Master Project

## Описание проекта

**Flower Delivery** — это интернет-магазин **Classic Floral Shop**. Проект позволяет пользователям приобретать цветы через веб-интерфейс, управлять заказами и получать уведомления через интеграцию с Telegram-ботом. Административная панель предоставляет возможности для сотрудников магазина управлять заказами и просматривать аналитику продаж.

Проект реализован на Django и включает взаимодействие с Telegram-ботом для улучшения пользовательского опыта и упрощения администрирования.

### Основные функции проекта:

#### Регистрация и управление пользователями
- **Регистрация и аутентификация**:
  - Пользователи могут зарегистрироваться, указав уникальные логин и пароль.
  - Доступна аутентификация через форму входа с возможностью восстановления пароля.

- **Управление профилем пользователя**:
  - Пользователи могут редактировать свой профиль, добавляя дополнительную информацию:
    - Имя, фамилия и отчество.
    - Электронная почта.
    - Дата рождения.
  - Доступна регистрация в Telegram-боте через сайт для получения уведомлений.

#### Каталог товаров
- **Просмотр каталога букетов**:
  - Пользователи могут просматривать доступные букеты с фотографиями, описанием и ценой.
  - Каждый букет имеет детальную страницу с подробной информацией и возможностью оставить отзыв.

- **Отзывы о букетах**:
  - Пользователи могут оставлять отзывы о приобретенных букетах, указывая рейтинг и комментарий.
  - Отзывы отображаются на странице каждого букета.

#### Корзина покупок
- **Управление корзиной**:
  - Добавление букетов в корзину с указанием количества.
  - Изменение количества товаров в корзине и удаление позиций.
  - Автоматический пересчет итоговой стоимости в зависимости от количества товаров.

#### Управление заказами
- **Создание и оформление заказа**:
  - Пользователи могут оформить заказ, указав количество товаров, адрес доставки, контактный телефон и желаемую дату/время доставки.
  - Поддержка ввода дополнительной информации (например, пожелания к букету или инструкции для курьера).

- **История заказов**:
  - Пользователи могут просматривать историю своих заказов с указанием статуса каждого заказа.

- **Изменение статусов заказов (только для сотрудников магазина)**:
  - Сотрудники магазина могут изменять статус заказа (например, «Ожидает подтверждения», «В пути», «Доставлен»).
  - Все изменения статуса фиксируются в истории заказов и могут быть просмотрены через административную панель.

#### Интеграция с Telegram-ботом
- **Регистрация в боте**:
  - Пользователи могут зарегистрироваться в Telegram-боте через сайт, чтобы получать уведомления о заказах.
  - Процесс регистрации происходит через команду `/start` с параметром `user_id`, передаваемым из сайта.

- **Уведомления о статусе заказов**:
  - Бот уведомляет пользователей об изменении статуса заказа (например, «Заказ доставлен»).

- **Администраторская функциональность**:
  - Администраторы могут просматривать аналитику продаж через бот.
  - Аналитика включает общее количество заказов, выручку и детализацию по периодам.

- **Просмотр аналитики**:
  - Доступна только администраторам через нажатие инлайн-кнопок в Telegram.
  - Включает графики продаж и текстовые отчеты за выбранный период (неделя, месяц, год).

## Документация

Проект включает подробную документацию, расположенную в папке `DOCS`. Ознакомьтесь с разделами:

- [Установка и настройка](./DOCS/INSTALLATION.md)  
  Содержит инструкции по установке, настройке и запуску проекта. Определяет минимальные системные требования и шаги для настройки окружения и запуска приложения.

- [Использование](./DOCS/USAGE.md)  
  Описывает основные функции проекта, включая управление пользователями, создание заказов, использование корзины и интеграцию с Telegram-ботом.

- [Архитектура проекта](./DOCS/ARCHITECTURE.md)  
  Описывает архитектуру и структуру проекта, а также взаимодействие компонентов (Django-сервер, Telegram-бот, клиентская часть).

- [Оптимизация](./DOCS/OPTIMIZATION.md)  
  В данном разделе собраны предложения по оптимизации, но они пока не реализованы. Проект стабильно функционирует в текущем виде, однако, при необходимости, оптимизации могут улучшить производительность и расширить функционал.

- [Решение проблем](./DOCS/TROUBLESHOOTING.md)  
  Содержит список распространенных проблем и их решений. Помогает решить ошибки, возникающие при запуске и использовании проекта, а также включает советы по устранению неполадок.

- [Содействие развитию проекта](./DOCS/CONTRIBUTING.md)  
  Правила и рекомендации для разработчиков, желающих внести свой вклад в развитие проекта. Описывает процесс форка, создания новой ветки, тестирования и отправки изменений.

## Начало работы
Для быстрого старта ознакомьтесь с [установкой и настройкой](./DOCS/INSTALLATION.md) проекта.

## Лицензия
Проект лицензируется под [MIT License](./LICENSE).

## Разработчик
Проект разработан **Eduard Ibatullin** с применением **ChatGPT**. Если у вас есть вопросы или предложения, свяжитесь со нами:

- Email: e.ibatullin@gmail.com
- Telegram: [@eduard_e_i](https://t.me/eduard_e_i)

Мы всегда рады обратной связи и готовы обсудить возможности улучшения проекта!
