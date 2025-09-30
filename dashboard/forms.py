from django import forms
from .models import LicensePlate

class CarImageForm(forms.ModelForm):
    class Meta:
        model = LicensePlate
        fields = ['car_image']  # แค่รูป
