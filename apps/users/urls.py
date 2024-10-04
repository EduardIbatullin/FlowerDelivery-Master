# apps/users/urls.py

from django.urls import path  # Импорт функции path для определения маршрутов URL-адресов

from .views import (
    CustomLoginView,                   # Представление для входа пользователя
    CustomLogoutView,                  # Представление для выхода пользователя
    register_view,                     # Представление для регистрации нового пользователя
    profile_view,                      # Представление для отображения профиля пользователя
    edit_profile_view,                 # Представление для редактирования профиля пользователя
    register_bot,                      # Представление для регистрации бота
    delete_account,                    # Представление для удаления аккаунта пользователя
    logout_view,                       # Представление для выхода пользователя
    save_telegram_id,                  # Представление для сохранения Telegram ID
    get_user_data,                     # Представление для получения данных пользователя
    get_user_data_by_telegram_id       # Представление для получения данных пользователя по Telegram ID
)

app_name = 'users'  # Устанавливаем пространство имен для приложения

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='auth/login.html'), name='login'),  # Страница входа пользователя
    path('logout/', logout_view, name='logout'),  # Страница выхода пользователя
    path('register/', register_view, name='register'),  # Страница регистрации нового пользователя
    path('profile/', profile_view, name='profile'),  # Страница профиля пользователя
    path('edit-profile/', edit_profile_view, name='edit_profile'),  # Страница редактирования профиля пользователя
    path('register-bot/', register_bot, name='register_bot'),  # Страница регистрации бота
    path('delete-account/', delete_account, name='delete_account'),  # Страница удаления аккаунта пользователя
    path('save_telegram_id/', save_telegram_id, name='save_telegram_id'),  # Сохранение Telegram ID пользователя
    path('get_user_data/', get_user_data, name='get_user_data'),  # Получение данных пользователя
    path('get_user_data_by_telegram_id/', get_user_data_by_telegram_id, name='get_user_data_by_telegram_id'),  # Получение данных пользователя по Telegram ID
]

"""
Описание URL-маршрутов:

1. `login` — Отображает страницу входа пользователя.
   - URL: `/login/`
   - Представление: `CustomLoginView.as_view(template_name='auth/login.html')`.

2. `logout` — Выполняет выход пользователя из системы.
   - URL: `/logout/`
   - Представление: `logout_view`.

3. `register` — Отображает страницу регистрации нового пользователя.
   - URL: `/register/`
   - Представление: `register_view`.

4. `profile` — Отображает страницу профиля текущего пользователя.
   - URL: `/profile/`
   - Представление: `profile_view`.

5. `edit_profile` — Отображает страницу редактирования профиля пользователя.
   - URL: `/edit-profile/`
   - Представление: `edit_profile_view`.

6. `register_bot` — Отображает страницу регистрации бота.
   - URL: `/register-bot/`
   - Представление: `register_bot`.

7. `delete_account` — Выполняет удаление аккаунта пользователя.
   - URL: `/delete-account/`
   - Представление: `delete_account`.

8. `save_telegram_id` — Сохраняет Telegram ID пользователя.
   - URL: `/save_telegram_id/`
   - Представление: `save_telegram_id`.

9. `get_user_data` — Предоставляет данные пользователя.
   - URL: `/get_user_data/`
   - Представление: `get_user_data`.

10. `get_user_data_by_telegram_id` — Предоставляет данные пользователя по Telegram ID.
    - URL: `/get_user_data_by_telegram_id/`
    - Представление: `get_user_data_by_telegram_id`.
"""
