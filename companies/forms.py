# companies/forms.py
from django import forms
from .models import Company
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm

class CompanyRegistrationForm(UserCreationForm):
    """Form for company registration"""
    company_name = forms.CharField(max_length=100, required=True)
    registration_number = forms.CharField(max_length=50, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    logo = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'company_name', 
                  'registration_number', 'address', 'phone_number', 'logo']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        if commit:
            user.save()
            company = Company(
                user=user,
                company_name=self.cleaned_data['company_name'],
                registration_number=self.cleaned_data['registration_number'],
                address=self.cleaned_data['address'],
                logo=self.cleaned_data.get('logo')
            )
            company.save()
        return user

class CompanyProfileForm(forms.ModelForm):
    """Form for editing company profile"""
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = Company
        fields = ['company_name', 'address', 'logo']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['email'].initial = self.user.email
            self.fields['phone_number'].initial = self.user.phone_number
    
    def save(self, commit=True):
        company = super().save(commit=False)
        if self.user:
            self.user.email = self.cleaned_data['email']
            self.user.phone_number = self.cleaned_data['phone_number']
            self.user.save()
        if commit:
            company.save()
        return company