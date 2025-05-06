# trips/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Trip, Passenger, Vehicle
from .forms import TripForm, PassengerForm, PassengerFormSet, VehicleForm
from payments.models import Payment, PaymentRate
import uuid

@login_required
def vehicle_list(request):
    """List all vehicles for a company"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    vehicles = Vehicle.objects.filter(company=request.user.company)
    return render(request, 'trips/vehicle_list.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    """Add a new vehicle"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.company = request.user.company
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('trips:vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'trips/add_vehicle.html', {'form': form})

@login_required
def edit_vehicle(request, vehicle_id):
    """Edit a vehicle"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, company=request.user.company)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('trips:vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'trips/edit_vehicle.html', {'form': form, 'vehicle': vehicle})

@login_required
def delete_vehicle(request, vehicle_id):
    """Delete a vehicle"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, company=request.user.company)
    
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully!')
        return redirect('trips:vehicle_list')
    
    return render(request, 'trips/delete_vehicle.html', {'vehicle': vehicle})

@login_required
def create_trip(request):
    """Create a new trip"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = TripForm(request.POST, company=request.user.company)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.company = request.user.company
            trip.save()
            
            # Get current payment rate
            rate = PaymentRate.objects.latest('effective_from')
            
            # Create a payment record for this trip
            payment = Payment(
                company=request.user.company,
                trip=trip,
                amount=rate.amount,
                reference=f"PAY-{uuid.uuid4().hex[:8].upper()}"
            )
            payment.save()
            
            messages.success(request, 'Trip created successfully! Please add passengers.')
            return redirect('trips:add_passenger', trip_id=trip.id)
    else:
        form = TripForm(company=request.user.company)
    
    return render(request, 'trips/create_trip.html', {'form': form})

@login_required
def trip_list(request):
    """List all trips for a company"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    trips = Trip.objects.filter(company=request.user.company).order_by('-created_at')
    return render(request, 'trips/trip_list.html', {'trips': trips})

@login_required
def trip_detail(request, trip_id):
    """View trip details"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    trip = get_object_or_404(Trip, id=trip_id, company=request.user.company)
    passengers = trip.passengers.all()
    payment = Payment.objects.filter(trip=trip).first()
    
    return render(request, 'trips/trip_detail.html', {
        'trip': trip,
        'passengers': passengers,
        'payment': payment
    })

@login_required
def edit_trip(request, trip_id):
    """Edit a trip"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    trip = get_object_or_404(Trip, id=trip_id, company=request.user.company)
    
    if trip.status != 'scheduled':
        messages.error(request, 'Cannot edit a trip that has already departed or completed.')
        return redirect('trips:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        form = TripForm(request.POST, instance=trip, company=request.user.company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trip updated successfully!')
            return redirect('trips:trip_detail', trip_id=trip.id)
    else:
        form = TripForm(instance=trip, company=request.user.company)
    
    return render(request, 'trips/edit_trip.html', {'form': form, 'trip': trip})

@login_required
def delete_trip(request, trip_id):
    """Delete a trip"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    trip = get_object_or_404(Trip, id=trip_id, company=request.user.company)
    
    if trip.status != 'scheduled':
        messages.error(request, 'Cannot delete a trip that has already departed or completed.')
        return redirect('trips:trip_detail', trip_id=trip.id)
    
    if request.method == 'POST':
        trip.delete()
        messages.success(request, 'Trip deleted successfully!')
        return redirect('trips:trip_list')
    
    return render(request, 'trips/delete_trip.html', {'trip': trip})

@login_required
def add_passenger(request, trip_id):
    """Add passengers to a trip"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    trip = get_object_or_404(Trip, id=trip_id, company=request.user.company)
    
    if request.method == 'POST':
        formset = PassengerFormSet(request.POST, instance=trip)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Passengers added successfully!')
            
            if 'add_more' in request.POST:
                return redirect('trips:add_passenger', trip_id=trip.id)
            else:
                return redirect('trips:trip_detail', trip_id=trip.id)
    else:
        formset = PassengerFormSet(instance=trip)
    
    return render(request, 'trips/add_passenger.html', {
        'formset': formset,
        'trip': trip
    })