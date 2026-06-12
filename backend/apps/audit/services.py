"""Audit service skeleton.

Business-state changes must call this service server-side. Frontend requests
must never be trusted to create their own audit trail.
"""

from __future__ import annotations

from typing import Any


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
        # Sprint 0 skeleton. Sprint 1 wires this to AuditEvent + code generation.
        return None
