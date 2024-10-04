# apps/analytics/urls.py

from django.urls import path  # Импорт path для создания URL-маршрутов

from .views import analytics_dashboard, update_analytics, get_analytics_data  # Импорт представлений для управления аналитикой


# Установка пространства имен для приложения аналитики
app_name = 'analytics'

# Определение URL-маршрутов для приложения аналитики
urlpatterns = [
    path('', analytics_dashboard, name='analytics_dashboard'),
    path('update/', update_analytics, name='update_analytics'),
    path('get_analytics_data/', get_analytics_data, name='get_analytics_data'),
]

"""
Описание URL-маршрутов:

1. `analytics_dashboard` — Отображает панель аналитики с данными о продажах и выручке.
2. `update_analytics` — Обрабатывает обновление данных аналитики (например, перерасчет статистики).
3. `get_analytics_data` — Возвращает данные аналитики в формате JSON для использования в ботах и других клиентах.
"""
