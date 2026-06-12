"""Audit event foundation for server-side accountability."""

import uuid

from django.conf import settings
from django.db import models


class AuditAction(models.TextChoices):
    CREATE = "create", "Create"
    UPDATE_DRAFT = "update_draft", "Update Draft"
    POST = "post", "Post"
    CANCEL = "cancel", "Cancel"
    ADJUST = "adjust", "Adjust"
    APPROVE = "approve", "Approve"
    REJECT = "reject", "Reject"
    LOGIN = "login", "Login"
    LOGOUT = "logout", "Logout"
    EXPORT = "export", "Export"
    PRINT_QR = "print_qr", "Print QR"
    SCAN_QR = "scan_qr", "Scan QR"
    OVERRIDE = "override", "Override"
    DELETE_DRAFT = "delete_draft", "Delete Draft"


class AuditEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=40, unique=True)
    table_name = models.CharField(max_length=128)
    record_id = models.UUIDField(null=True, blank=True)
    record_code = models.CharField(max_length=64, blank=True)
    action = models.CharField(max_length=32, choices=AuditAction.choices)
    old_value_json = models.JSONField(null=True, blank=True)
    new_value_json = models.JSONField(null=True, blank=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=64, blank=True)
    device_id = models.CharField(max_length=128, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["table_name", "record_id"], name="audit_audit_table_n_4d4074_idx"),
            models.Index(fields=["record_code"], name="audit_audit_record__ee581f_idx"),
            models.Index(fields=["action"], name="audit_audit_action_4d6b83_idx"),
            models.Index(fields=["actor"], name="audit_audit_actor_i_dbbd12_idx"),
            models.Index(fields=["action_time"], name="audit_audit_action__0acaa3_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.code} {self.action}"
