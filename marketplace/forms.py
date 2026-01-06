from django import forms
from .models import Waste

class WasteForm(forms.ModelForm):
    class Meta:
        model = Waste
        fields = [
            'waste_type',
            'description',
            'weight_kg',
            'image',
        ]
