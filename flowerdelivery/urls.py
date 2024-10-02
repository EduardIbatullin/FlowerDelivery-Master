# flowerdelivery/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view
from apps.users.views import save_telegram_id

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('cart/', include('apps.cart.urls', namespace='cart')),
    path('catalog/', include('apps.catalog.urls', namespace='catalog')),
    path('management/', include('apps.management.urls', namespace='management')),
    path('orders/', include('apps.orders.urls', namespace='orders')),
    path('reviews/', include('apps.reviews.urls', namespace='reviews')),
    path('users/', include('apps.users.urls', namespace='users')),

    # Специальный маршрут для интеграции с ботом
    path('users/save_telegram_id/', save_telegram_id, name='save_telegram_id'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
