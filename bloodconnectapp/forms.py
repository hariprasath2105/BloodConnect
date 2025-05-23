from django import forms
from django.contrib.auth import get_user_model
from .models import DonorProfile, BloodRequest

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    """Form for user registration"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'user_type', 'first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'country']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'user_type': forms.Select(choices=[('donor', 'Donor'), ('receiver', 'Receiver')])
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'city', 'state', 'country']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class DonorProfileForm(forms.ModelForm):
    """Form for donor registration"""
    class Meta:
        model = DonorProfile
        fields = ['blood_group', 'gender', 'age', 'medical_conditions']
        widgets = {
            'medical_conditions': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18:
            raise forms.ValidationError('You must be at least 18 years old to donate blood.')
        if age > 65:
            raise forms.ValidationError('You must be under 65 years old to donate blood.')
        return age

class BloodRequestForm(forms.ModelForm):
    """Form for creating blood requests"""
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'units_needed', 'hospital_name', 'hospital_address', 'reason', 'urgency', 'required_date']
        widgets = {
            'hospital_address': forms.Textarea(attrs={'rows': 3}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'required_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def clean_units_needed(self):
        units = self.cleaned_data.get('units_needed')
        if units < 1:
            raise forms.ValidationError('You must request at least 1 unit of blood.')
        if units > 10:
            raise forms.ValidationError('You cannot request more than 10 units at once.')
        return units 