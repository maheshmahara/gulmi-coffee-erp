from rest_framework import serializers

from .models import LocationType, StorageLocation


class StorageLocationSerializer(serializers.ModelSerializer):
    location_type = serializers.ChoiceField(choices=LocationType.choices)
    parent_location_code = serializers.CharField(source="parent_location.code", read_only=True)

    class Meta:
        model = StorageLocation
        fields = [
            "id",
            "code",
            "location_name",
            "location_type",
            "parent_location",
            "parent_location_code",
            "active",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "code", "parent_location_code", "created_at", "updated_at"]
