# Generated manually for Sprint 0 foundation.

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
            name="AuditEvent",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=40, unique=True)),
                ("table_name", models.CharField(max_length=128)),
                ("record_id", models.UUIDField(blank=True, null=True)),
                ("record_code", models.CharField(blank=True, max_length=64)),
                ("action", models.CharField(choices=[("create", "Create"), ("update_draft", "Update Draft"), ("post", "Post"), ("cancel", "Cancel"), ("adjust", "Adjust"), ("approve", "Approve"), ("reject", "Reject"), ("login", "Login"), ("logout", "Logout"), ("export", "Export"), ("print_qr", "Print QR"), ("scan_qr", "Scan QR"), ("override", "Override"), ("delete_draft", "Delete Draft")], max_length=32)),
                ("old_value_json", models.JSONField(blank=True, null=True)),
                ("new_value_json", models.JSONField(blank=True, null=True)),
                ("action_time", models.DateTimeField(auto_now_add=True)),
                ("ip_address", models.CharField(blank=True, max_length=64)),
                ("device_id", models.CharField(blank=True, max_length=128)),
                ("notes", models.TextField(blank=True)),
                ("actor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(model_name="auditevent", index=models.Index(fields=["table_name", "record_id"], name="audit_audit_table_n_4d4074_idx")),
        migrations.AddIndex(model_name="auditevent", index=models.Index(fields=["record_code"], name="audit_audit_record__ee581f_idx")),
        migrations.AddIndex(model_name="auditevent", index=models.Index(fields=["action"], name="audit_audit_action_4d6b83_idx")),
        migrations.AddIndex(model_name="auditevent", index=models.Index(fields=["actor"], name="audit_audit_actor_i_dbbd12_idx")),
        migrations.AddIndex(model_name="auditevent", index=models.Index(fields=["action_time"], name="audit_audit_action__0acaa3_idx")),
    ]
