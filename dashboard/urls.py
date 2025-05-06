# dashboard/urls.py
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('company/', views.company_dashboard, name='company'),
    path('stats/', views.dashboard_stats, name='stats'),
]