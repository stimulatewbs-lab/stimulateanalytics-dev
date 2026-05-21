from django.urls import path

from sms.webhooks import delivery_webhook
from .views import *

urlpatterns = [

    path(
        '',
        sms_dashboard,
        name='sms_dashboard'
    ),

    path(
        'send/',
        send_sms,
        name='send_sms'
    ),

    path(
        'history/',
        sms_history,
        name='sms_history'
    ),
    path(
    'webhook/delivery/',
    delivery_webhook,
    name='delivery_webhook'
),
]