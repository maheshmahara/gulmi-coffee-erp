from decimal import Decimal

from rest_framework import serializers

from apps.common.services import SensitiveFieldFilterService

from .models import CoffeeItemType, Farmer, FarmerType, Lot, LotStatus, ProcurementReceipt, ProcurementStatus


class FarmerSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ["id", "code", "farmer_name", "phone", "village", "district", "farmer_type", "active"]


class FarmerSerializer(serializers.ModelSerializer):
    farmer_type = serializers.ChoiceField(choices=FarmerType.choices)

    class Meta:
        model = Farmer
        fields = [
            "id",
            "code",
            "farmer_name",
            "father_or_family_name",
            "phone",
            "village",
            "municipality",
            "district",
            "ward_no",
            "gps_location",
            "photo_url",
            "bank_or_wallet",
            "farmer_type",
            "active",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "code", "created_at", "updated_at"]

    def validate(self, attrs):
        active = attrs.get("active", getattr(self.instance, "active", True))
        phone = attrs.get("phone", getattr(self.instance, "phone", ""))
        if active and not phone:
            raise serializers.ValidationError({"phone": "Phone is required for active farmers."})
        return attrs


class LotSerializer(serializers.ModelSerializer):
    farmer_id = serializers.PrimaryKeyRelatedField(source="farmer", queryset=Farmer.objects.filter(active=True), write_only=True)
    farmer = FarmerSummarySerializer(read_only=True)
    item_type = serializers.ChoiceField(choices=CoffeeItemType.choices)
    status = serializers.ChoiceField(choices=LotStatus.choices, required=False)

    class Meta:
        model = Lot
        fields = [
            "id",
            "code",
            "farmer",
            "farmer_id",
            "item_type",
            "harvest_year",
            "status",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "code", "farmer", "created_at", "updated_at"]


class ProcurementReceiptSerializer(serializers.ModelSerializer):
    lot_id = serializers.PrimaryKeyRelatedField(source="lot", queryset=Lot.objects.select_related("farmer").all(), write_only=True)
    lot_code = serializers.CharField(source="lot.code", read_only=True)
    farmer = FarmerSummarySerializer(read_only=True)
    farmer_code = serializers.CharField(source="farmer.code", read_only=True)
    farmer_name = serializers.CharField(source="farmer.farmer_name", read_only=True)
    received_by_name = serializers.CharField(source="received_by.full_name", read_only=True)
    posted_by_name = serializers.CharField(source="posted_by.full_name", read_only=True)

    class Meta:
        model = ProcurementReceipt
        fields = [
            "id",
            "code",
            "lot",
            "lot_id",
            "lot_code",
            "farmer",
            "farmer_code",
            "farmer_name",
            "item_type",
            "gross_kg",
            "tare_kg",
            "net_kg",
            "rate_npr",
            "total_npr",
            "received_at",
            "received_by",
            "received_by_name",
            "status",
            "posted_at",
            "posted_by",
            "posted_by_name",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "code",
            "lot",
            "lot_code",
            "farmer",
            "farmer_code",
            "farmer_name",
            "item_type",
            "net_kg",
            "total_npr",
            "status",
            "posted_at",
            "posted_by",
            "received_by_name",
            "posted_by_name",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        gross_kg = attrs.get("gross_kg", getattr(self.instance, "gross_kg", None))
        tare_kg = attrs.get("tare_kg", getattr(self.instance, "tare_kg", Decimal("0")))
        if gross_kg is not None and gross_kg <= 0:
            raise serializers.ValidationError({"gross_kg": "Gross kg must be greater than zero."})
        if tare_kg is not None and tare_kg < 0:
            raise serializers.ValidationError({"tare_kg": "Tare kg cannot be negative."})
        if gross_kg is not None and tare_kg is not None and gross_kg <= tare_kg:
            raise serializers.ValidationError({"gross_kg": "Gross kg must be greater than tare kg."})
        return attrs

    def to_representation(self, instance):
        payload = super().to_representation(instance)
        role = self.context.get("role", "")
        return SensitiveFieldFilterService().filter_payload(payload, role)


class ProcurementPostSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    code = serializers.CharField(read_only=True)
    status = serializers.ChoiceField(choices=ProcurementStatus.choices, read_only=True)
    posted_at = serializers.DateTimeField(read_only=True)
