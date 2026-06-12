from django.contrib import admin

from .models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("code", "table_name", "record_code", "action", "actor", "action_time")
    list_filter = ("action", "table_name")
    search_fields = ("code", "record_code", "table_name", "notes")
    readonly_fields = [field.name for field in AuditEvent._meta.fields]
