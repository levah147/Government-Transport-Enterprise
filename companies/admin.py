from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'registration_number', 'is_active', 'date_joined')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('company_name', 'registration_number', 'user__username')
    readonly_fields = ('date_joined',)
