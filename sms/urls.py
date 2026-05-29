from django.urls import path

from .views import (
    sms_dashboard,
    send_sms,
    sms_history,
)

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

]