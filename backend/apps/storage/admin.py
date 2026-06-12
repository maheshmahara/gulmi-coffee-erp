from django.contrib import admin

from .models import StorageLocation


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ("code", "location_name", "location_type", "parent_location", "active")
    list_filter = ("location_type", "active")
    search_fields = ("code", "location_name")
