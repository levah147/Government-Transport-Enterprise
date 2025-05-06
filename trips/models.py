# trips/models.py
from django.db import models
from companies.models import Company

class Vehicle(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)  # e.g., Bus, Car, etc.
    capacity = models.IntegerField()
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.company.company_name}"

class Trip(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    departure_location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(
        ('scheduled', 'Scheduled'),
        ('departed', 'Departed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ), default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.company.company_name}: {self.departure_location} to {self.destination} on {self.departure_time}"

class Passenger(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='passengers')
    full_name = models.CharField(max_length=100)
    id_type = models.CharField(max_length=50, choices=(
        ('national_id', 'National ID'),
        ('voters_card', 'Voters Card'),
        ('drivers_license', 'Drivers License'),
        ('passport', 'International Passport'),
        ('others', 'Others')
    ))
    id_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_phone = models.CharField(max_length=20)
    
    def __str__(self):
        return self.full_name