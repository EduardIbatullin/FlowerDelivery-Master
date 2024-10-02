# apps/users/tests/test_urls.py

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.users.views import (
    CustomLoginView,
    logout_view,
    register_view,
    profile_view,
    edit_profile_view,
    register_bot,
    delete_account,
    save_telegram_id,
    get_user_data,
    get_user_data_by_telegram_id
)


class UsersUrlsTest(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('users:login')
        self.assertEqual(resolve(url).func.view_class, CustomLoginView)

    def test_logout_url_resolves(self):
        url = reverse('users:logout')
        self.assertEqual(resolve(url).func, logout_view)

    def test_register_url_resolves(self):
        url = reverse('users:register')
        self.assertEqual(resolve(url).func, register_view)

    def test_profile_url_resolves(self):
        url = reverse('users:profile')
        self.assertEqual(resolve(url).func, profile_view)

    def test_edit_profile_url_resolves(self):
        url = reverse('users:edit_profile')
        self.assertEqual(resolve(url).func, edit_profile_view)

    def test_register_bot_url_resolves(self):
        url = reverse('users:register_bot')
        self.assertEqual(resolve(url).func, register_bot)

    def test_delete_account_url_resolves(self):
        url = reverse('users:delete_account')
        self.assertEqual(resolve(url).func, delete_account)

    def test_save_telegram_id_url_resolves(self):
        url = reverse('users:save_telegram_id')
        self.assertEqual(resolve(url).func, save_telegram_id)

    def test_get_user_data_url_resolves(self):
        url = reverse('users:get_user_data')
        self.assertEqual(resolve(url).func, get_user_data)

    def test_get_user_data_by_telegram_id_url_resolves(self):
        url = reverse('users:get_user_data_by_telegram_id')
        self.assertEqual(resolve(url).func, get_user_data_by_telegram_id)
