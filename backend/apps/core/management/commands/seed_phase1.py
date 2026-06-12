from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.storage.models import StorageLocation


class Command(BaseCommand):
    help = "Seed Phase-1 default users and storage locations."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="ChangeMe123!", help="Default password for seeded users.")

    @transaction.atomic
    def handle(self, *args, **options):
        password = options["password"]
        self.seed_users(password)
        self.seed_locations()
        self.stdout.write(self.style.SUCCESS("Phase-1 seed data ready."))

    def seed_users(self, password):
        User = get_user_model()
        users = [
            ("USER-2026-000001", "admin", "Admin User", "9800000001", "admin", True),
            ("USER-2026-000002", "manager", "Manager User", "9800000002", "manager", True),
            ("USER-2026-000003", "quality", "Quality User", "9800000003", "quality", False),
            ("USER-2026-000004", "storage", "Storage User", "9800000004", "storage", False),
            ("USER-2026-000005", "viewer", "Viewer User", "9800000005", "viewer", False),
        ]
        for code, username, full_name, phone, role, is_staff in users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "code": code,
                    "full_name": full_name,
                    "phone": phone,
                    "role": role,
                    "active": True,
                    "is_staff": is_staff,
                    "is_superuser": role == "admin",
                },
            )
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f"Created user {username} / {code}")

    def seed_locations(self):
        rows = [
            ("WH-001", "Main Warehouse", "warehouse", None, "Main storage building"),
            ("RACK-PAR-001", "Parchment Rack 1", "rack", "WH-001", "For parchment bags"),
            ("RACK-PAR-002", "Parchment Rack 2", "rack", "WH-001", "For parchment bags"),
            ("RACK-GRN-001", "Green Bean Rack 1", "rack", "WH-001", "For green beans"),
            ("HOLD-001", "Defect/Recheck Area", "hold_area", "WH-001", "Risk or rejected bags"),
            ("DRY-001", "Solar Drying Area", "drying_area", None, "Drying area"),
            ("PROD-HULL-001", "Hulling Area", "production_area", None, "Hulling input area"),
        ]

        created_by = get_user_model().objects.filter(username="admin").first()
        for code, name, location_type, parent_code, notes in rows:
            parent = StorageLocation.objects.filter(code=parent_code).first() if parent_code else None
            location, created = StorageLocation.objects.get_or_create(
                code=code,
                defaults={
                    "location_name": name,
                    "location_type": location_type,
                    "parent_location": parent,
                    "active": True,
                    "notes": notes,
                    "created_by": created_by,
                    "updated_by": created_by,
                },
            )
            if created:
                self.stdout.write(f"Created location {location.code} / {location.location_name}")
