# trips/urls.py
from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('create/', views.create_trip, name='create_trip'),
    path('list/', views.trip_list, name='trip_list'),
    path('<int:trip_id>/', views.trip_detail, name='trip_detail'),
    path('<int:trip_id>/edit/', views.edit_trip, name='edit_trip'),
    path('<int:trip_id>/delete/', views.delete_trip, name='delete_trip'),
    path('<int:trip_id>/passengers/add/', views.add_passenger, name='add_passenger'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('vehicles/add/', views.add_vehicle, name='add_vehicle'),
    path('vehicles/<int:vehicle_id>/edit/', views.edit_vehicle, name='edit_vehicle'),
    path('vehicles/<int:vehicle_id>/delete/', views.delete_vehicle, name='delete_vehicle'),
]