# payments/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment, PaymentRate
from trips.models import Trip
from django.utils import timezone

@login_required
def make_payment(request, trip_id):
    """Process payment for a trip"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    trip = get_object_or_404(Trip, id=trip_id, company=request.user.company)
    payment = get_object_or_404(Payment, trip=trip)
    
    if payment.status == 'completed':
        messages.info(request, 'Payment has already been completed for this trip.')
        return redirect('trips:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        # Simulate payment processing
        # In a real application, this would integrate with a payment gateway
        payment.status = 'completed'
        payment.save()
        
        # Update trip status
        trip.status = 'departed'
        trip.save()
        
        messages.success(request, 'Payment completed successfully!')
        return redirect('trips:trip_detail', trip_id=trip.id)
    
    return render(request, 'payments/make_payment.html', {
        'trip': trip,
        'payment': payment
    })

@login_required
def payment_history(request):
    """View payment history"""
    if request.user.user_type == 'company':
        payments = Payment.objects.filter(company=request.user.company).order_by('-payment_date')
    elif request.user.user_type == 'admin':
        payments = Payment.objects.all().order_by('-payment_date')
    else:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    return render(request, 'payments/payment_history.html', {'payments': payments})

@login_required
def payment_detail(request, payment_id):
    """View payment details"""
    if request.user.user_type == 'company':
        payment = get_object_or_404(Payment, id=payment_id, company=request.user.company)
    elif request.user.user_type == 'admin':
        payment = get_object_or_404(Payment, id=payment_id)
    else:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    return render(request, 'payments/payment_detail.html', {'payment': payment})

@login_required
def payment_rates(request):
    """View and manage payment rates (admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Only administrators can manage payment rates.')
        return redirect('dashboard:index')
    
    rates = PaymentRate.objects.all().order_by('-effective_from')
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description', '')
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            new_rate = PaymentRate(
                amount=amount,
                description=description,
                effective_from=timezone.now()
            )
            new_rate.save()
            messages.success(request, f'New payment rate of ₦{amount} set successfully!')
            return redirect('payments:payment_rates')
        except ValueError:
            messages.error(request, 'Please enter a valid amount.')
    
    return render(request, 'payments/payment_rates.html', {'rates': rates})