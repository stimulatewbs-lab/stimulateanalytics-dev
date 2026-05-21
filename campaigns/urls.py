from django.urls import path
from . import views

urlpatterns = [
    path('', views.campaign_list, name='campaign_list'),

    path('create/', views.campaign_create, name='campaign_create'),

    path('update/<int:pk>/', views.campaign_update, name='campaign_update'),

    path('delete/<int:pk>/', views.campaign_delete, name='campaign_delete'),
]