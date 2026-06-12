from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AppUser


@admin.register(AppUser)
class AppUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Gulmi ERP", {"fields": ("code", "full_name", "phone", "role", "active")}),
    )
    list_display = ("username", "code", "full_name", "phone", "role", "active", "is_staff")
    list_filter = ("role", "active", "is_staff", "is_superuser")
    search_fields = ("username", "code", "full_name", "phone", "email")
