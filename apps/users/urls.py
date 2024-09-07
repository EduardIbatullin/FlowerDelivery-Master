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
    logout_view
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile/', profile_view, name='profile'),
    path('edit-profile/', edit_profile_view, name='edit_profile'),
    path('register-bot/', register_bot, name='register_bot'),
    path('delete-account/', delete_account, name='delete_account'),
]
