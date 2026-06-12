"""Shared service skeletons for Phase-1 business logic."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class GeneratedCode:
    prefix: str
    year: int
    sequence: int

    @property
    def value(self) -> str:
        return f"{self.prefix}-{self.year}-{self.sequence:06d}"


class CodeGeneratorService:
    """Central place for readable ERP business code generation.

    Sprint 0 only defines the contract. Sprint 1+ will back this with a
    database sequence/counter so codes remain unique under concurrency.
    """

    def preview(self, prefix: str, sequence: int = 1, at: datetime | None = None) -> str:
        year = (at or datetime.now()).year
        return GeneratedCode(prefix=prefix, year=year, sequence=sequence).value

    def next_for_model(self, *, model, prefix: str, at: datetime | None = None) -> str:
        """Generate a readable code for Sprint 1.

        This count-based implementation is acceptable for the single-user Sprint 1
        foundation. A locked counter table should replace it before high-concurrency
        production use.
        """

        year = (at or datetime.now()).year
        sequence = model.objects.filter(code__startswith=f"{prefix}-{year}-").count() + 1
        return GeneratedCode(prefix=prefix, year=year, sequence=sequence).value


class SensitiveFieldFilterService:
    """Backend-only guard for Admin/Manager financial field visibility."""

    allowed_roles = {"admin", "manager"}
    sensitive_fields = {"rate_npr", "total_npr", "payment", "cost", "margin", "profit"}

    def can_view_sensitive_fields(self, role: str) -> bool:
        return role in self.allowed_roles

    def filter_payload(self, payload: dict, role: str) -> dict:
        if self.can_view_sensitive_fields(role):
            return payload
        return {key: (None if key in self.sensitive_fields else value) for key, value in payload.items()}
