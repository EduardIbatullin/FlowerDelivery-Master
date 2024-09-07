from django.urls import path
from .views import sales_report_view, profit_analysis_view

urlpatterns = [
    path('sales-report/', sales_report_view, name='sales_report'),  # Отчет о продажах
    path('profit-analysis/', profit_analysis_view, name='profit_analysis'),  # Анализ прибыли
]
