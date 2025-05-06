# companies/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyRegistrationForm, CompanyProfileForm
from .models import Company
from trips.models import Trip, Vehicle
from payments.models import Payment
from emergency.models import Emergency
from django.contrib.auth import login

def company_register(request):
    
    """Register a new transport company"""
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to Government Transport Enterprise, {user.company.company_name}!')
            return redirect('companies:dashboard')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'companies/register.html', {'form': form})

@login_required
def company_dashboard(request):
    """Company dashboard view"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied. You are not registered as a transport company.')
        return redirect('dashboard:index')
    
    company = request.user.company
    recent_trips = Trip.objects.filter(company=company).order_by('-created_at')[:5]
    recent_payments = Payment.objects.filter(company=company).order_by('-payment_date')[:5]
    recent_emergencies = Emergency.objects.filter(company=company).order_by('-reported_at')[:3]
    vehicles = Vehicle.objects.filter(company=company).count()
    
    context = {
        'company': company,
        'recent_trips': recent_trips,
        'recent_payments': recent_payments,
        'recent_emergencies': recent_emergencies,
        'total_vehicles': vehicles,
        'total_trips': Trip.objects.filter(company=company).count(),
        'payments_completed': Payment.objects.filter(company=company, status='completed').count(),
        'active_emergencies': Emergency.objects.filter(company=company).exclude(status='resolved').count()
    }
    return render(request, 'companies/dashboard.html', context)

@login_required
def company_profile(request):
    """View company profile"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied. You are not registered as a transport company.')
        return redirect('dashboard:index')
    
    company = request.user.company
    return render(request, 'companies/profile.html', {'company': company})

@login_required
def edit_company_profile(request):
    """Edit company profile"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied. You are not registered as a transport company.')
        return redirect('dashboard:index')
    
    company = request.user.company
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated successfully!')
            return redirect('companies:profile')
    else:
        form = CompanyProfileForm(instance=company, user=request.user)
    return render(request, 'companies/edit_profile.html', {'form': form})