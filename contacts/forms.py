from django import forms
from .models import Contact, ContactGroup


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "email",
        ]


class ContactGroupForm(forms.ModelForm):
    class Meta:
        model = ContactGroup
        fields = [
            "name",
            "description",
            "contacts",
        ]

        widgets = {
            "contacts": forms.CheckboxSelectMultiple(),
        }