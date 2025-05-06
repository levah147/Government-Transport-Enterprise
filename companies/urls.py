# companies/urls.py
from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('register/', views.company_register, name='register'),
    path('dashboard/', views.company_dashboard, name='dashboard'),
    path('profile/', views.company_profile, name='profile'),
    path('profile/edit/', views.edit_company_profile, name='edit_profile'),
]
