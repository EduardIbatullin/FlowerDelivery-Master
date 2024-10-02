# apps/users/urls.py

from django.urls import path
from .views import (
    CustomLoginView,
    CustomLogoutView,
    register_view,
    profile_view,
    edit_profile_view,
    register_bot,
    delete_account,
    logout_view,
    save_telegram_id,
    get_user_data,
    get_user_data_by_telegram_id
)

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('register-bot/', register_bot, name='register_bot'),
    path('delete-account/', delete_account, name='delete_account'),
    path('save_telegram_id/', save_telegram_id, name='save_telegram_id'),
    path('get_user_data/', get_user_data, name='get_user_data'),
    path('get_user_data_by_telegram_id/', get_user_data_by_telegram_id, name='get_user_data_by_telegram_id'),  # Добавляем маршрут
]
