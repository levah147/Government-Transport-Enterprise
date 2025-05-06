# trips/forms.py
from django import forms
from .models import Trip, Passenger, Vehicle
from django.utils import timezone

class VehicleForm(forms.ModelForm):
    """Form for adding/editing vehicles"""
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'vehicle_type', 'capacity']

class TripForm(forms.ModelForm):
    """Form for creating/editing trips"""
    departure_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        initial=timezone.now
    )
    
    class Meta:
        model = Trip
        fields = ['vehicle', 'departure_location', 'destination', 'departure_time']
    
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if self.company:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(company=self.company)

class PassengerForm(forms.ModelForm):
    """Form for adding passengers to a trip"""
    class Meta:
        model = Passenger
        fields = ['full_name', 'id_type', 'id_number', 'phone_number', 'next_of_kin', 'next_of_kin_phone']

PassengerFormSet = forms.inlineformset_factory(
    Trip, Passenger, form=PassengerForm,
    extra=1, can_delete=True, max_num=50
)