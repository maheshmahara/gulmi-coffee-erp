import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class FarmerType(models.TextChoices):
    FARMER = "farmer", "Farmer"
    COLLECTOR = "collector", "Collector"
    COOPERATIVE = "cooperative", "Cooperative"
    SUPPLIER = "supplier", "Supplier"


class CoffeeItemType(models.TextChoices):
    FRESH_CHERRY = "fresh_cherry", "Fresh Cherry"
    DRY_CHERRY = "dry_cherry", "Dry Cherry"
    PARCHMENT = "parchment", "Parchment"
    GREEN_BEAN = "green_bean", "Green Bean"


class LotStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    RECEIVED = "received", "Received"
    QUALITY_PENDING = "quality_pending", "Quality Pending"
    APPROVED = "approved", "Approved"
    HOLD = "hold", "Hold"
    BAGGED = "bagged", "Bagged"
    CLOSED = "closed", "Closed"


class ProcurementStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    POSTED = "posted", "Posted"
    CANCELLED = "cancelled", "Cancelled"


class Farmer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=40, unique=True)
    farmer_name = models.CharField(max_length=255)
    father_or_family_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    village = models.CharField(max_length=128)
    municipality = models.CharField(max_length=128, blank=True)
    district = models.CharField(max_length=128)
    ward_no = models.CharField(max_length=16, blank=True)
    gps_location = models.CharField(max_length=128, blank=True)
    photo_url = models.URLField(blank=True)
    bank_or_wallet = models.CharField(max_length=255, blank=True)
    farmer_type = models.CharField(max_length=32, choices=FarmerType.choices, default=FarmerType.FARMER)
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_farmers")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_farmers")

    class Meta:
        indexes = [
            models.Index(fields=["farmer_name"], name="procurement_farmer__b9b317_idx"),
            models.Index(fields=["phone"], name="procurement_phone_2572b3_idx"),
            models.Index(fields=["village"], name="procurement_village_16e23d_idx"),
            models.Index(fields=["district"], name="procurement_distric_54f76b_idx"),
            models.Index(fields=["farmer_type"], name="procurement_farmer__61e227_idx"),
            models.Index(fields=["active"], name="procurement_active_4a2c97_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.code} {self.farmer_name}"


class Lot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=40, unique=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.PROTECT, related_name="lots")
    item_type = models.CharField(max_length=32, choices=CoffeeItemType.choices)
    harvest_year = models.PositiveIntegerField()
    status = models.CharField(max_length=32, choices=LotStatus.choices, default=LotStatus.DRAFT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_lots")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_lots")

    class Meta:
        indexes = [
            models.Index(fields=["farmer"], name="procurement_farmer__85e43e_idx"),
            models.Index(fields=["item_type"], name="procurement_item_ty_17199a_idx"),
            models.Index(fields=["harvest_year"], name="procurement_harvest_9ae527_idx"),
            models.Index(fields=["status"], name="procurement_status_54fb31_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.code} {self.item_type}"


class ProcurementReceipt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=40, unique=True)
    lot = models.ForeignKey(Lot, on_delete=models.PROTECT, related_name="procurements")
    farmer = models.ForeignKey(Farmer, on_delete=models.PROTECT, related_name="procurements")
    item_type = models.CharField(max_length=32, choices=CoffeeItemType.choices)
    gross_kg = models.DecimalField(max_digits=12, decimal_places=3)
    tare_kg = models.DecimalField(max_digits=12, decimal_places=3, default=Decimal("0.000"))
    net_kg = models.DecimalField(max_digits=12, decimal_places=3)
    rate_npr = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_npr = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    received_at = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="received_procurements")
    status = models.CharField(max_length=32, choices=ProcurementStatus.choices, default=ProcurementStatus.DRAFT)
    posted_at = models.DateTimeField(null=True, blank=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="posted_procurements")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="created_procurements")
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="updated_procurements")

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(gross_kg__gt=0), name="procurement_gross_kg_positive"),
            models.CheckConstraint(check=models.Q(tare_kg__gte=0), name="procurement_tare_kg_non_negative"),
            models.CheckConstraint(check=models.Q(gross_kg__gt=models.F("tare_kg")), name="procurement_gross_gt_tare"),
        ]
        indexes = [
            models.Index(fields=["farmer"], name="procurement_farmer__08c100_idx"),
            models.Index(fields=["lot"], name="procurement_lot_id_805976_idx"),
            models.Index(fields=["item_type"], name="procurement_item_ty_7fac54_idx"),
            models.Index(fields=["status"], name="procurement_status_64dc6f_idx"),
            models.Index(fields=["received_at"], name="procurement_receive_86e5db_idx"),
        ]

    @property
    def is_posted(self) -> bool:
        return self.status == ProcurementStatus.POSTED

    def calculate_amounts(self) -> None:
        self.gross_kg = Decimal(str(self.gross_kg))
        self.tare_kg = Decimal(str(self.tare_kg))
        self.rate_npr = Decimal(str(self.rate_npr)) if self.rate_npr is not None else None
        self.net_kg = self.gross_kg - self.tare_kg
        self.total_npr = self.net_kg * self.rate_npr if self.rate_npr is not None else None

    def save(self, *args, **kwargs):
        if self.lot_id:
            self.farmer_id = self.lot.farmer_id
            self.item_type = self.lot.item_type
        self.calculate_amounts()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.code} {self.net_kg}kg"
