

# Register your models here.
from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):

    list_display = (
        'first_name',
        'last_name',
        'phone_number',
        'email'
    )

    search_fields = (
        'first_name',
        'last_name',
        'phone_number'
    )