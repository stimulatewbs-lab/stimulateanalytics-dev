from django import forms
from contacts.models import ContactGroup

class SendSMSForm(forms.Form):

    sender_id = forms.CharField(
        max_length=20
    )

    group = forms.ModelChoiceField(
        queryset=ContactGroup.objects.all()
    )

    message = forms.CharField(
        widget=forms.Textarea
    )