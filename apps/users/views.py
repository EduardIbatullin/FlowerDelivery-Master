# apps/users/views.py

import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import UserProfileForm, CustomUserCreationForm
from .models import Profile

# Инициализация логгера
logger = logging.getLogger(__name__)

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('catalog:catalog_list')


@login_required
def profile_view(request):
    user = request.user
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    telegram_id_value = profile.telegram_id
    logger.info(f"Telegram ID for user {user.username}: {telegram_id_value}")

    profile_data = {
        'last_name': user.last_name or '—',
        'first_name': user.first_name or '—',
        'patronymic': user.patronymic or '—',
        'birth_date': user.birth_date or '—',
        'email': profile.email or '—',
        'telegram_id': profile.telegram_id,
        'telegram_status': 'Зарегистрирован в телеграм-боте магазина' if profile.telegram_id else 'Регистрация в телеграм-боте'
    }

    return render(request, 'users/profile.html', {'profile_data': profile_data})


@login_required
def edit_profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.email = form.cleaned_data.get('email')
            profile.telegram_id = form.cleaned_data.get('telegram_id')
            profile.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=user, initial={'email': profile.email, 'telegram_id': profile.telegram_id})

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def register_bot(request):
    messages.info(request, 'Вы успешно зарегистрировались в Telegram-боте.')
    return redirect('users:profile')


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
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@csrf_exempt
def save_telegram_id(request):
    """
    Сохраняет telegram_id в профиле пользователя на основе user_id, полученного от бота.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')
            user_id = data.get('user_id')

            logger.info(f"Получен запрос на сохранение telegram_id: {telegram_id} для user_id: {user_id}")

            if telegram_id and user_id:
                try:
                    # Ищем пользователя по user_id
                    user = User.objects.get(id=user_id)
                    profile = user.profile

                    # Проверка, не зарегистрирован ли уже этот telegram_id
                    if profile.telegram_id == telegram_id:
                        return JsonResponse({'status': 'success', 'message': 'Этот Telegram ID уже привязан к вашему профилю.'})

                    profile.telegram_id = telegram_id
                    profile.save()

                    logger.info(f"telegram_id {telegram_id} успешно сохранен для пользователя {user.username}")
                    return JsonResponse({'status': 'success', 'message': 'Telegram ID успешно сохранен'})
                except User.DoesNotExist:
                    logger.warning(f"Пользователь с ID {user_id} не найден")
                    return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'})
            else:
                logger.warning(f"Некорректные данные: telegram_id={telegram_id}, user_id={user_id}")
                return JsonResponse({'status': 'error', 'message': 'Некорректные данные'})
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка при декодировании JSON: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Ошибка формата данных'})
        except Exception as e:
            logger.error(f"Произошла ошибка: {str(e)}")
            return JsonResponse({'status': 'error', 'message': 'Ошибка при обработке данных'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})


@csrf_exempt
def get_user_data(request):
    """
    Возвращает данные пользователя по user_id.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')

            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                    return JsonResponse({
                        'status': 'success',
                        'first_name': user.first_name,
                        'username': user.username,
                        'is_admin': user.is_staff or user.is_superuser,
                    })
                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Пользователь не найден'}, status=404)
            else:
                return JsonResponse({'status': 'error', 'message': 'ID пользователя не предоставлен'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Неправильный формат JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=405)


@csrf_exempt
def get_user_data_by_telegram_id(request):
    """
    Возвращает данные пользователя по telegram_id.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            telegram_id = data.get('telegram_id')

            if telegram_id:
                try:
                    # Используем filter() вместо get() для предотвращения MultipleObjectsReturned
                    profiles = Profile.objects.filter(telegram_id=telegram_id)

                    if profiles.exists():
                        # Получаем первый профиль из списка, если есть несколько
                        profile = profiles.first()
                        user = profile.user
                        return JsonResponse({
                            'status': 'success',
                            'user_data': {
                                'first_name': user.first_name,
                                'is_admin': user.is_staff or user.is_superuser,
                            }
                        })
                    else:
                        return JsonResponse(
                            {'status': 'error', 'message': 'Пользователь с данным Telegram ID не найден'}, status=404)
                except Profile.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Пользователь с данным Telegram ID не найден'},
                                        status=404)
            else:
                return JsonResponse({'status': 'error', 'message': 'Telegram ID не предоставлен'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Неправильный формат JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'}, status=405)