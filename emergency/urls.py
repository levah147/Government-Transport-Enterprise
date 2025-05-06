# emergency/urls.py
from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('report/', views.report_emergency, name='report'),
    path('list/', views.emergency_list, name='list'),
    path('<int:emergency_id>/', views.emergency_detail, name='detail'),
    path('<int:emergency_id>/update/', views.update_emergency, name='update'),
]