from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="accounts_dashboard"),
    path("place-bet/", views.place_bet, name="place_bet"),
]