from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import phonenumbers
import pycountry

from .models import CustomerProfile

from django.core.exceptions import ValidationError
def get_country_choices():
    countries = [
        (country.name, country.name)
        for country in pycountry.countries
    ]

    return sorted(countries, key=lambda item: item[1])


def get_phone_code_choices():
    choices = []

    for country in pycountry.countries:
        calling_code = phonenumbers.country_code_for_region(
            country.alpha_2
        )

        if not calling_code:
            continue

        choices.append(
            (
                country.alpha_2,
                f"{country.name} (+{calling_code})",
            )
        )

    return sorted(choices, key=lambda item: item[1])


class CustomerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First name",
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last name",
    )

    email = forms.EmailField(
        required=True,
        label="Email address",
    )

    phone_country_code = forms.ChoiceField(
        required=True,
        label="Phone country",
        choices=get_phone_code_choices(),
        widget=forms.Select(),
    )

    phone_number = forms.CharField(
        max_length=15,
        required=True,
        label="Phone number",
        widget=forms.TextInput(
            attrs={
                "placeholder": "788123456",
                "inputmode": "numeric",
                "autocomplete": "tel-national",
            }
        ),
    )

    date_of_birth = forms.DateField(
        required=True,
        label="Date of birth",
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={
                "type": "date",
                "autocomplete": "bday",
            },
        ),
    )

    country = forms.ChoiceField(
        required=True,
        label="Country of residence",
        choices=get_country_choices(),
        widget=forms.Select(),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_country_code",
            "phone_number",
            "date_of_birth",
            "country",
            "password1",
            "password2",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        region = cleaned_data.get("phone_country_code")
        local_number = cleaned_data.get("phone_number")

        if region and local_number:
            try:
                parsed_number = phonenumbers.parse(
                    local_number,
                    region,
                )

                if not phonenumbers.is_valid_number(parsed_number):
                    self.add_error(
                        "phone_number",
                        "Enter a valid phone number for the selected country.",
                    )
                else:
                    full_number = phonenumbers.format_number(
                        parsed_number,
                        phonenumbers.PhoneNumberFormat.E164,
                    )

                    if CustomerProfile.objects.filter(
                        phone_number=full_number
                    ).exists():
                        self.add_error(
                            "phone_number",
                            "An account with this phone number already exists.",
                        )

                    cleaned_data["phone_number"] = full_number

            except phonenumbers.NumberParseException:
                self.add_error(
                    "phone_number",
                    "Enter a valid phone number.",
                )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            profile = user.customer_profile
            profile.phone_number = self.cleaned_data["phone_number"]
            profile.date_of_birth = self.cleaned_data["date_of_birth"]
            profile.country = self.cleaned_data["country"]
            profile.save()

        return user

def clean(self):
    cleaned_data = super().clean()

    password1 = cleaned_data.get("password1")
    password2 = cleaned_data.get("password2")

    if password1 and password2 and password1 != password2:
        raise ValidationError("The passwords do not match.")

    region = cleaned_data.get("phone_country_code")
    local_number = cleaned_data.get("phone_number")

    if region and local_number:
        try:
            parsed_number = phonenumbers.parse(
                local_number,
                region,
            )

            if not phonenumbers.is_valid_number(parsed_number):
                self.add_error(
                    "phone_number",
                    "Enter a valid phone number for the selected country.",
                )
            else:
                full_number = phonenumbers.format_number(
                    parsed_number,
                    phonenumbers.PhoneNumberFormat.E164,
                )

                if CustomerProfile.objects.filter(
                    phone_number=full_number
                ).exists():
                    self.add_error(
                        "phone_number",
                        "An account with this phone number already exists.",
                    )

                cleaned_data["phone_number"] = full_number

        except phonenumbers.NumberParseException:
            self.add_error(
                "phone_number",
                "Enter a valid phone number.",
            )

    return cleaned_data