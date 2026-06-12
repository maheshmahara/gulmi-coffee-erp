"""Audit service skeleton.

Business-state changes must call this service server-side. Frontend requests
must never be trusted to create their own audit trail.
"""

from __future__ import annotations

from typing import Any

from apps.common.services import CodeGeneratorService

from .models import AuditEvent


class AuditService:
    def record(
        self,
        *,
        action: str,
        table_name: str,
        actor: Any = None,
        record_id: Any = None,
        record_code: str = "",
        old_value: dict | None = None,
        new_value: dict | None = None,
        notes: str = "",
    ) -> None:
        code = CodeGeneratorService().next_for_model(model=AuditEvent, prefix="AUDIT")
        AuditEvent.objects.create(
            code=code,
            table_name=table_name,
            record_id=record_id,
            record_code=record_code,
            action=action,
            old_value_json=old_value,
            new_value_json=new_value,
            actor=actor if getattr(actor, "is_authenticated", False) else None,
            notes=notes,
        )
