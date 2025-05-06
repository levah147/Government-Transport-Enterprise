
# payments/models.py
from django.db import models
from trips.models import Trip
from companies.models import Company

class PaymentRate(models.Model):
    """Model to store the configurable fee per trip"""
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)  # Default 500 Naira
    effective_from = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return f"₦{self.amount} (from {self.effective_from})"

class Payment(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='payments')
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ), default='pending')
    
    def __str__(self):
        return f"Payment of ₦{self.amount} for {self.trip}"