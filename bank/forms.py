from django import forms
from .models import Donor, BloodRequest

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = [
            'name',
            'age',
            'gender',
            'blood_group',
            'phone',
            'email',
            'address',
            'last_donation_date',
            'units_donated',  
        ]



class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'hospital_name', 'blood_group', 'units_requested', 'reason']
