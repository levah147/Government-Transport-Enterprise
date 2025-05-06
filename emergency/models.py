
# emergency/models.py
from django.db import models
from companies.models import Company
from trips.models import Trip

class Emergency(models.Model):
    EMERGENCY_TYPES = (
        ('accident', 'Accident'),
        ('breakdown', 'Vehicle Breakdown'),
        ('medical', 'Medical Emergency'),
        ('security', 'Security Threat'),
        ('other', 'Other')
    )
    
    EMERGENCY_STATUS = (
        ('reported', 'Reported'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    )
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='emergencies')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='emergencies', null=True, blank=True)
    emergency_type = models.CharField(max_length=20, choices=EMERGENCY_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=EMERGENCY_STATUS, default='reported')
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_emergency_type_display()} by {self.company.company_name}"