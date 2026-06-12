# Generated manually for Sprint 1 foundation.

import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="StorageLocation",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=40, unique=True)),
                ("location_name", models.CharField(max_length=255)),
                ("location_type", models.CharField(choices=[("warehouse", "Warehouse"), ("rack", "Rack"), ("drying_area", "Drying Area"), ("hold_area", "Hold Area"), ("production_area", "Production Area"), ("finished_goods", "Finished Goods")], max_length=32)),
                ("active", models.BooleanField(default=True)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_storage_locations", to=settings.AUTH_USER_MODEL)),
                ("parent_location", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="children", to="storage.storagelocation")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="updated_storage_locations", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="storagelocation", index=models.Index(fields=["location_type"], name="storage_sto_locatio_a41aae_idx")),
        migrations.AddIndex(model_name="storagelocation", index=models.Index(fields=["parent_location"], name="storage_sto_parent__dd7e1f_idx")),
        migrations.AddIndex(model_name="storagelocation", index=models.Index(fields=["active"], name="storage_sto_active_d10565_idx")),
    ]
