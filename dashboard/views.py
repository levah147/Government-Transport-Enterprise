# dashboard/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from companies.models import Company
from trips.models import Trip, Passenger, Vehicle
from payments.models import Payment
from emergency.models import Emergency
from django.db.models import Count, Sum, Q
from django.utils import timezone
import datetime

def index(request):
    """Landing page view"""
    if request.user.is_authenticated:
        if request.user.user_type == 'admin':
            return redirect('dashboard:admin')
        elif request.user.user_type == 'company':
            return redirect('dashboard:company')
    
    return render(request, 'dashboard/index.html')

@login_required
def admin_dashboard(request):
    """Admin dashboard view"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Only administrators can access this dashboard.')
        return redirect('dashboard:index')
    
    # Get statistics for display
    total_companies = Company.objects.filter(is_active=True).count()
    total_trips = Trip.objects.all().count()
    total_vehicles = Vehicle.objects.all().count()
    total_passengers = Passenger.objects.all().count()
    
    # Revenue statistics
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get today's date
    today = timezone.now().date()
    
    # Calculate today's statistics
    today_trips = Trip.objects.filter(departure_time__date=today).count()
    today_revenue = Payment.objects.filter(
        payment_date__date=today, 
        status='completed'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Recent activities
    recent_companies = Company.objects.order_by('-date_joined')[:5]
    recent_trips = Trip.objects.order_by('-created_at')[:5]
    recent_payments = Payment.objects.order_by('-payment_date')[:5]
    active_emergencies = Emergency.objects.filter(status__in=['reported', 'in_progress']).order_by('-reported_at')
    
    context = {
        'total_companies': total_companies,
        'total_trips': total_trips,
        'total_vehicles': total_vehicles,
        'total_passengers': total_passengers,
        'total_revenue': total_revenue,
        'today_trips': today_trips,
        'today_revenue': today_revenue,
        'recent_companies': recent_companies,
        'recent_trips': recent_trips,
        'recent_payments': recent_payments,
        'active_emergencies': active_emergencies,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def company_dashboard(request):
    """Redirect to company dashboard in companies app"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    return redirect('companies:dashboard')

@login_required
def dashboard_stats(request):
    """Generate statistics for dashboard"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    # Get date range from request, default to last 30 days
    days = int(request.GET.get('days', 30))
    end_date = timezone.now().date()
    start_date = end_date - datetime.timedelta(days=days)
    
    # Generate date range
    date_range = [start_date + datetime.timedelta(days=x) for x in range((end_date-start_date).days + 1)]
    
    # Get trip counts by date
    trips_by_date = Trip.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).values('created_at__date').annotate(count=Count('id')).order_by('created_at__date')
    
    # Format trip data for chart
    trip_dates = [item['created_at__date'] for item in trips_by_date]
    trip_counts = [item['count'] for item in trips_by_date]
    
    # Get revenue by date
    revenue_by_date = Payment.objects.filter(
        payment_date__date__gte=start_date,
        payment_date__date__lte=end_date,
        status='completed'
    ).values('payment_date__date').annotate(total=Sum('amount')).order_by('payment_date__date')
    
    # Format revenue data for chart
    revenue_dates = [item['payment_date__date'] for item in revenue_by_date]
    revenue_amounts = [float(item['total']) for item in revenue_by_date]
    
    # Get top companies by trip count
    top_companies_by_trips = Company.objects.annotate(
        trip_count=Count('trips')
    ).order_by('-trip_count')[:10]
    
    # Get top companies by revenue
    top_companies_by_revenue = Company.objects.annotate(
        revenue=Sum('payments__amount', filter=Q(payments__status='completed'))
    ).filter(revenue__isnull=False).order_by('-revenue')[:10]
    
    context = {
        'days': days,
        'start_date': start_date,
        'end_date': end_date,
        'date_range': date_range,
        'trip_dates': trip_dates,
        'trip_counts': trip_counts,
        'revenue_dates': revenue_dates,
        'revenue_amounts': revenue_amounts,
        'top_companies_by_trips': top_companies_by_trips,
        'top_companies_by_revenue': top_companies_by_revenue,
    }
    
    return render(request, 'dashboard/stats.html', context)