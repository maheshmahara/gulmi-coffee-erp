# Generated for Gulmi Coffee ERP Phase 1 Sprint 2.

import django.db.models.deletion
import django.utils.timezone
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Farmer",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=40, unique=True)),
                ("farmer_name", models.CharField(max_length=255)),
                ("father_or_family_name", models.CharField(blank=True, max_length=255)),
                ("phone", models.CharField(blank=True, max_length=32)),
                ("village", models.CharField(max_length=128)),
                ("municipality", models.CharField(blank=True, max_length=128)),
                ("district", models.CharField(max_length=128)),
                ("ward_no", models.CharField(blank=True, max_length=16)),
                ("gps_location", models.CharField(blank=True, max_length=128)),
                ("photo_url", models.URLField(blank=True)),
                ("bank_or_wallet", models.CharField(blank=True, max_length=255)),
                ("farmer_type", models.CharField(choices=[("farmer", "Farmer"), ("collector", "Collector"), ("cooperative", "Cooperative"), ("supplier", "Supplier")], default="farmer", max_length=32)),
                ("active", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_farmers", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_farmers", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Lot",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=40, unique=True)),
                ("item_type", models.CharField(choices=[("fresh_cherry", "Fresh Cherry"), ("dry_cherry", "Dry Cherry"), ("parchment", "Parchment"), ("green_bean", "Green Bean")], max_length=32)),
                ("harvest_year", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("draft", "Draft"), ("received", "Received"), ("quality_pending", "Quality Pending"), ("approved", "Approved"), ("hold", "Hold"), ("bagged", "Bagged"), ("closed", "Closed")], default="draft", max_length=32)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_lots", to=settings.AUTH_USER_MODEL)),
                ("farmer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="lots", to="procurement.farmer")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_lots", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="ProcurementReceipt",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=40, unique=True)),
                ("item_type", models.CharField(choices=[("fresh_cherry", "Fresh Cherry"), ("dry_cherry", "Dry Cherry"), ("parchment", "Parchment"), ("green_bean", "Green Bean")], max_length=32)),
                ("gross_kg", models.DecimalField(decimal_places=3, max_digits=12)),
                ("tare_kg", models.DecimalField(decimal_places=3, default=Decimal("0.000"), max_digits=12)),
                ("net_kg", models.DecimalField(decimal_places=3, max_digits=12)),
                ("rate_npr", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("total_npr", models.DecimalField(blank=True, decimal_places=2, max_digits=14, null=True)),
                ("received_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("posted", "Posted"), ("cancelled", "Cancelled")], default="draft", max_length=32)),
                ("posted_at", models.DateTimeField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_procurements", to=settings.AUTH_USER_MODEL)),
                ("farmer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="procurements", to="procurement.farmer")),
                ("lot", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="procurements", to="procurement.lot")),
                ("posted_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="posted_procurements", to=settings.AUTH_USER_MODEL)),
                ("received_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="received_procurements", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_procurements", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="farmer", index=models.Index(fields=["farmer_name"], name="procurement_farmer__b9b317_idx")),
        migrations.AddIndex(model_name="farmer", index=models.Index(fields=["phone"], name="procurement_phone_2572b3_idx")),
        migrations.AddIndex(model_name="farmer", index=models.Index(fields=["village"], name="procurement_village_16e23d_idx")),
        migrations.AddIndex(model_name="farmer", index=models.Index(fields=["district"], name="procurement_distric_54f76b_idx")),
        migrations.AddIndex(model_name="farmer", index=models.Index(fields=["farmer_type"], name="procurement_farmer__61e227_idx")),
        migrations.AddIndex(model_name="farmer", index=models.Index(fields=["active"], name="procurement_active_4a2c97_idx")),
        migrations.AddIndex(model_name="lot", index=models.Index(fields=["farmer"], name="procurement_farmer__85e43e_idx")),
        migrations.AddIndex(model_name="lot", index=models.Index(fields=["item_type"], name="procurement_item_ty_17199a_idx")),
        migrations.AddIndex(model_name="lot", index=models.Index(fields=["harvest_year"], name="procurement_harvest_9ae527_idx")),
        migrations.AddIndex(model_name="lot", index=models.Index(fields=["status"], name="procurement_status_54fb31_idx")),
        migrations.AddConstraint(model_name="procurementreceipt", constraint=models.CheckConstraint(check=models.Q(("gross_kg__gt", 0)), name="procurement_gross_kg_positive")),
        migrations.AddConstraint(model_name="procurementreceipt", constraint=models.CheckConstraint(check=models.Q(("tare_kg__gte", 0)), name="procurement_tare_kg_non_negative")),
        migrations.AddConstraint(model_name="procurementreceipt", constraint=models.CheckConstraint(check=models.Q(("gross_kg__gt", models.F("tare_kg"))), name="procurement_gross_gt_tare")),
        migrations.AddIndex(model_name="procurementreceipt", index=models.Index(fields=["farmer"], name="procurement_farmer__08c100_idx")),
        migrations.AddIndex(model_name="procurementreceipt", index=models.Index(fields=["lot"], name="procurement_lot_id_805976_idx")),
        migrations.AddIndex(model_name="procurementreceipt", index=models.Index(fields=["item_type"], name="procurement_item_ty_7fac54_idx")),
        migrations.AddIndex(model_name="procurementreceipt", index=models.Index(fields=["status"], name="procurement_status_64dc6f_idx")),
        migrations.AddIndex(model_name="procurementreceipt", index=models.Index(fields=["received_at"], name="procurement_receive_86e5db_idx")),
    ]
