from django.urls import path

from .api_views import SMSListAPI

urlpatterns = [

    path(
        'messages/',
        SMSListAPI.as_view()
    ),
]