from django import forms
from .models import SMSMessage


class SMSForm(forms.ModelForm):

    class Meta:
        model = SMSMessage

        fields = [
            'campaign',
            'contact',
            'message',
        ]