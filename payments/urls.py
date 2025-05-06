# payments/urls.py
from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('trip/<int:trip_id>/', views.make_payment, name='make_payment'),
    path('history/', views.payment_history, name='payment_history'),
    path('<int:payment_id>/', views.payment_detail, name='payment_detail'),
    path('rates/', views.payment_rates, name='payment_rates'),
]