from django import forms
from .models import Package,Booking

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['user', 'membership_package', 'status']