from django.urls import path
from . import views

app_name = 'campaigns'

urlpatterns = [

    path(
        '',
        views.campaign_list,
        name='campaign_list'
    ),

    path(
        'create/',
        views.campaign_create,
        name='campaign_create'
    ),

    path(
        '<int:pk>/edit/',
        views.campaign_update,
        name='campaign_update'
    ),

    path(
        '<int:pk>/delete/',
        views.campaign_delete,
        name='campaign_delete'
    ),

]