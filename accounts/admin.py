from django.contrib import admin
from .models import User, AuditLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'is_active',
        'is_staff'
    )

    list_filter = (
        'role',
        'is_active'
    )

    search_fields = (
        'username',
        'email'
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'ip_address',
        'created_at'
    )

    search_fields = (
        'action',
    )

    list_filter = (
        'created_at',
    )