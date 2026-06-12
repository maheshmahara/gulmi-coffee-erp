"""User and role foundation for Phase 1."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    QUALITY = "quality", "Quality"
    STORAGE = "storage", "Storage"
    PRODUCTION = "production", "Production"
    SALES = "sales", "Sales"
    VIEWER = "viewer", "Viewer"


class AppUser(AbstractUser):
    """Custom user model with Gulmi Coffee ERP role metadata."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=32, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=32, blank=True)
    role = models.CharField(max_length=32, choices=UserRole.choices, default=UserRole.VIEWER)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["full_name"]

    def save(self, *args, **kwargs):
        if self.full_name and not self.first_name:
            first, *rest = self.full_name.split(" ", 1)
            self.first_name = first
            self.last_name = rest[0] if rest else ""
        self.is_active = self.active
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.code or self.username
