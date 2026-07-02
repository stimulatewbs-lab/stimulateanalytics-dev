from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [

    path('', views.dashboard, name='reports_dashboard'),



    path(
        'campaign/<int:pk>/',
        views.campaign_report,
        name='campaign_report'
    ),

]