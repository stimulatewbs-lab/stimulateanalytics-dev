from django import forms

from .models import Contact, ContactGroup


class ContactForm(forms.ModelForm):

    class Meta:

        model = Contact

        fields = [
            'name',
            'phone',
           
            'group'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),

            'group': forms.Select(attrs={
                'class': 'form-select'
            }),

        }


class ContactGroupForm(forms.ModelForm):

    class Meta:

        model = ContactGroup

        fields = ['name']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Group Name'
            }),

        }


class CSVUploadForm(forms.Form):

    csv_file = forms.FileField(

        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })

    )