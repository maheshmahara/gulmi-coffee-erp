import uuid

from django.conf import settings
from django.db import models


class LocationType(models.TextChoices):
    WAREHOUSE = "warehouse", "Warehouse"
    RACK = "rack", "Rack"
    DRYING_AREA = "drying_area", "Drying Area"
    HOLD_AREA = "hold_area", "Hold Area"
    PRODUCTION_AREA = "production_area", "Production Area"
    FINISHED_GOODS = "finished_goods", "Finished Goods"


class StorageLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=40, unique=True)
    location_name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=32, choices=LocationType.choices)
    parent_location = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children")
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_storage_locations")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_storage_locations")

    class Meta:
        indexes = [
            models.Index(fields=["location_type"]),
            models.Index(fields=["parent_location"]),
            models.Index(fields=["active"]),
        ]

    def __str__(self) -> str:
        return f"{self.code} {self.location_name}"
