# apps/analytics/urls.py

from django.urls import path
from .views import analytics_dashboard, update_analytics, get_analytics_data

app_name = 'analytics'

urlpatterns = [
    path('', analytics_dashboard, name='analytics_dashboard'),
    path('update/', update_analytics, name='update_analytics'),
    path('get_analytics_data/', get_analytics_data, name='get_analytics_data'),
]
