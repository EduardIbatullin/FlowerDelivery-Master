# flowerdelivery/urls.py

from django.contrib import admin  # Импорт модуля для управления админ-панелью Django
from django.urls import path, include  # Импорт функций path и include для маршрутизации URL-адресов
from django.conf import settings  # Импорт настроек проекта
from django.conf.urls.static import static  # Импорт функции для работы с медиа- и статическими файлами

from .views import home_view  # Импорт представления для домашней страницы
from apps.users.views import save_telegram_id  # Импорт представления для сохранения Telegram ID пользователя


# Основные маршруты проекта
urlpatterns = [
    path('', home_view, name='home'),  # Главная страница сайта
    path('admin/', admin.site.urls),  # Админ-панель Django для управления данными проекта
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),  # Маршруты для приложения аналитики
    path('cart/', include('apps.cart.urls', namespace='cart')),  # Маршруты для приложения корзины
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),  # Маршруты для приложения каталога товаров
    path('management/', include('apps.management.urls', namespace='management')),  # Маршруты для приложения управления заказами
    path('orders/', include('apps.orders.urls', namespace='orders')),  # Маршруты для работы с заказами пользователей
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),  # Маршруты для работы с отзывами пользователей
    path('users/', include('apps.users.urls', namespace='users')),  # Маршруты для управления пользователями

    # Специальный маршрут для интеграции с ботом
    path('users/save_telegram_id/', save_telegram_id, name='save_telegram_id'),  # Путь для сохранения Telegram ID пользователя
]

# Добавление маршрутов для медиа- и статических файлов в режиме отладки (DEBUG)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Маршрут для отображения медиа-файлов
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Маршрут для отображения статических файлов

"""
Описание URL-маршрутов:

1. `home` — Отображает главную страницу сайта.
   - URL: `/`
   - Представление: `home_view`.

2. `admin` — Отображает админ-панель Django для управления данными проекта.
   - URL: `/admin/`
   - Представление: `admin.site.urls`.

3. `analytics` — Отображает страницы приложения аналитики.
   - URL: `/analytics/`
   - Маршрутизация: `apps.analytics.urls`.

4. `cart` — Отображает страницы корзины товаров.
   - URL: `/cart/`
   - Маршрутизация: `apps.cart.urls`.

5. `catalog` — Отображает страницы каталога товаров.
   - URL: `/catalog/`
   - Маршрутизация: `apps.catalog.urls`.

6. `management` — Отображает страницы управления заказами.
   - URL: `/management/`
   - Маршрутизация: `apps.management.urls`.

7. `orders` — Отображает страницы заказов.
   - URL: `/orders/`
   - Маршрутизация: `apps.orders.urls`.

8. `reviews` — Отображает страницы отзывов.
   - URL: `/reviews/`
   - Маршрутизация: `apps.reviews.urls`.

9. `users` — Отображает страницы управления пользователями.
   - URL: `/users/`
   - Маршрутизация: `apps.users.urls`.

10. `save_telegram_id` — Сохраняет Telegram ID пользователя при интеграции с ботом.
    - URL: `/users/save_telegram_id/`
    - Представление: `save_telegram_id`.

11. `static` и `media` — Обрабатывают маршруты для отображения статических и медиа-файлов в режиме отладки (DEBUG).
    - URL: `/static/`, `/media/`
    - Маршрутизация: `static()`.

"""
