from django.urls import path
from .views import billing

urlpatterns = [
    path('', billing, name='billing')
]