from django.urls import path
from.import views

urlpatterns = [
    path('', views.contact_groups, name='contact_groups'),

    path('create-group/', views.create_group, name='create_group'),

    path('upload/<int:group_id>/', views.upload_contacts, name='upload_contacts'),
    path('', views.contact_list, name='contact_list'),

    path('create/',
        views.create_contact,
        name='create_contact'
    ),

]