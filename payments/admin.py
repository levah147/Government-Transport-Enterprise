from django.contrib import admin
from .models import Payment, PaymentRate

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'company', 
        'trip', 
        'amount', 
        'status', 
        'payment_date', 
        'reference'
    )
    list_filter = ('status', 'payment_date')
    search_fields = ('company__company_name', 'trip__id', 'reference')
    readonly_fields = ('payment_date',)

@admin.register(PaymentRate)
class PaymentRateAdmin(admin.ModelAdmin):
    list_display = ('amount', 'effective_from', 'description')
    readonly_fields = ('effective_from',)
