from django import forms
from .models import Campaign
from contacts.models import Contact, ContactGroup

class CampaignForm(forms.ModelForm):

    class Meta:
        model = Campaign

        fields = [
            'name',
            'message',
            'status',
        ]

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'groups',
        ]


class ContactGroupForm(forms.ModelForm):

    class Meta:
        model = ContactGroup

        fields = [
            'name',
            'description',
        ]