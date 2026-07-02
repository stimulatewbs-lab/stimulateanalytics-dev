from django.contrib import admin
from .models import SMSMessage


@admin.register(SMSMessage)
class SMSMessageAdmin(admin.ModelAdmin):

    list_display = (
        'campaign',
        'contact',
        'status',
        'created_at',
        'sent_at',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'message',
        'contact__phone_number',
        'campaign__name',
    )