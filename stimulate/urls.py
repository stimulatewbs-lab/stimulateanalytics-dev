from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('admin/', admin.site.urls),
    
    # WEB APPS
    path('', include('dashboard.urls')),
    path('campaigns/', include('campaigns.urls')),
    path('contacts/', include('contacts.urls')),
    path('sms/', include('sms.urls')),
    path('reports/', include('reports.urls')),
    path('billing/', include('billing.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # JWT AUTH API
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
]