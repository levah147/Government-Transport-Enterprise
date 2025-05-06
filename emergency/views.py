
# emergency/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Emergency
from .forms import EmergencyForm, EmergencyUpdateForm
from django.utils import timezone

@login_required
def report_emergency(request):
    """Report a new emergency"""
    if request.user.user_type != 'company':
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = EmergencyForm(request.POST, company=request.user.company)
        if form.is_valid():
            emergency = form.save(commit=False)
            emergency.company = request.user.company
            emergency.save()
            messages.success(request, 'Emergency reported successfully! Our team will contact you shortly.')
            return redirect('emergency:list')
    else:
        form = EmergencyForm(company=request.user.company)
    
    return render(request, 'emergency/report.html', {'form': form})

@login_required
def emergency_list(request):
    """List all emergencies"""
    if request.user.user_type == 'company':
        emergencies = Emergency.objects.filter(company=request.user.company).order_by('-reported_at')
    elif request.user.user_type == 'admin':
        emergencies = Emergency.objects.all().order_by('-reported_at')
    else:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    return render(request, 'emergency/list.html', {'emergencies': emergencies})

@login_required
def emergency_detail(request, emergency_id):
    """View emergency details"""
    if request.user.user_type == 'company':
        emergency = get_object_or_404(Emergency, id=emergency_id, company=request.user.company)
    elif request.user.user_type == 'admin':
        emergency = get_object_or_404(Emergency, id=emergency_id)
    else:
        messages.error(request, 'Access denied.')
        return redirect('dashboard:index')
    
    return render(request, 'emergency/detail.html', {'emergency': emergency})

@login_required
def update_emergency(request, emergency_id):
    """Update emergency status (admin only)"""
    if request.user.user_type != 'admin':
        messages.error(request, 'Access denied. Only administrators can update emergency status.')
        return redirect('dashboard:index')
    
    emergency = get_object_or_404(Emergency, id=emergency_id)
    
    if request.method == 'POST':
        form = EmergencyUpdateForm(request.POST, instance=emergency)
        if form.is_valid():
            updated_emergency = form.save(commit=False)
            if updated_emergency.status == 'resolved' and not updated_emergency.resolved_at:
                updated_emergency.resolved_at = timezone.now()
            updated_emergency.save()
            messages.success(request, 'Emergency status updated successfully!')
            return redirect('emergency:detail', emergency_id=emergency.id)
    else:
        form = EmergencyUpdateForm(instance=emergency)
    
    return render(request, 'emergency/update.html', {'form': form, 'emergency': emergency})