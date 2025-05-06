# emergency/forms.py
from django import forms
from .models import Emergency
from trips.models import Trip

class EmergencyForm(forms.ModelForm):
    """Form for reporting emergencies"""
    trip = forms.ModelChoiceField(queryset=Trip.objects.none(), required=False)
    
    class Meta:
        model = Emergency
        fields = ['emergency_type', 'description', 'location', 'trip']
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company', None)
        super().__init__(*args, **kwargs)
        if company:
            self.fields['trip'].queryset = Trip.objects.filter(
                company=company, 
                status__in=['departed', 'scheduled']
            )

class EmergencyUpdateForm(forms.ModelForm):
    """Form for updating emergency status"""
    class Meta:
        model = Emergency
        fields = ['status', 'description']
