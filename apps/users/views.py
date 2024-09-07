# apps/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog_list')


@login_required
def profile_view(request):
    user = request.user
    profile_data = {
        'last_name': user.last_name or '—',
        'first_name': user.first_name or '—',
        'patronymic': user.patronymic or '—',
        'birth_date': user.birth_date or '—',
    }
    return render(request, 'users/profile.html', {'profile_data': profile_data})


@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def register_bot(request):
    messages.info(request, 'Вы успешно зарегистрировались в Telegram-боте.')
    return redirect('profile')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, 'Ваш аккаунт был успешно удален.')
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно. Теперь вы можете войти в свой аккаунт.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
