from django import forms
from .models import Campaign


class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign

        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Campaign Name'
            })
        }