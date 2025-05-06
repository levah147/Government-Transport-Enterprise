# companies/models.py
from django.db import models
from accounts.models import User

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    company_name = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.company_name