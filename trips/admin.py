from django.contrib import admin
from .models import Vehicle, Trip, Passenger

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'company', 'vehicle_type', 'capacity')
    list_filter = ('vehicle_type', 'company')
    search_fields = ('vehicle_number', 'company__company_name')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('company', 'vehicle', 'departure_location', 'destination', 'departure_time', 'status')
    list_filter = ('status', 'departure_time', 'company')
    search_fields = ('company__company_name', 'departure_location', 'destination')
    autocomplete_fields = ['company', 'vehicle']
    readonly_fields = ('created_at',)

@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'trip', 'id_type', 'id_number', 'phone_number')
    list_filter = ('id_type',)
    search_fields = ('full_name', 'id_number', 'trip__departure_location', 'trip__destination')
    autocomplete_fields = ['trip']
