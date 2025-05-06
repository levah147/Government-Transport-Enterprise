from django.contrib import admin
from .models import Emergency

@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = (
        'emergency_type', 
        'company', 
        'trip', 
        'location', 
        'status', 
        'reported_at', 
        'resolved_at'
    )
    list_filter = ('status', 'emergency_type', 'reported_at')
    search_fields = ('company__company_name', 'description', 'location')
    readonly_fields = ('reported_at',)
