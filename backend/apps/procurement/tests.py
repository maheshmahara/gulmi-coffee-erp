from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from apps.accounts.models import AppUser, UserRole

from .models import Farmer, Lot, LotStatus, ProcurementReceipt, ProcurementStatus


class ProcurementWorkflowApiTests(TestCase):
    def setUp(self):
        self.admin = AppUser.objects.create_user(username="admin", password="pass12345", full_name="Admin User", role=UserRole.ADMIN)
        self.viewer = AppUser.objects.create_user(username="viewer", password="pass12345", full_name="Viewer User", role=UserRole.VIEWER)
        self.client = APIClient()

    def test_admin_can_create_and_post_procurement(self):
        self.client.force_authenticate(self.admin)
        farmer_response = self.client.post(
            "/api/v1/farmers",
            {
                "farmer_name": "Ram Bahadur",
                "phone": "9800000000",
                "village": "Tamghas",
                "district": "Gulmi",
                "farmer_type": "farmer",
            },
            format="json",
        )
        self.assertEqual(farmer_response.status_code, 201)

        lot_response = self.client.post(
            "/api/v1/lots",
            {
                "farmer_id": farmer_response.data["data"]["id"],
                "item_type": "parchment",
                "harvest_year": 2026,
            },
            format="json",
        )
        self.assertEqual(lot_response.status_code, 201)

        procurement_response = self.client.post(
            "/api/v1/procurements",
            {
                "lot_id": lot_response.data["data"]["id"],
                "gross_kg": "705.000",
                "tare_kg": "5.000",
                "rate_npr": "1300.00",
            },
            format="json",
        )
        self.assertEqual(procurement_response.status_code, 201)
        self.assertEqual(procurement_response.data["data"]["net_kg"], "700.000")
        self.assertEqual(procurement_response.data["data"]["total_npr"], "910000.00")

        procurement_id = procurement_response.data["data"]["id"]
        post_response = self.client.post(f"/api/v1/procurements/{procurement_id}/post", {}, format="json")
        self.assertEqual(post_response.status_code, 200)
        self.assertEqual(post_response.data["data"]["status"], ProcurementStatus.POSTED)

        procurement = ProcurementReceipt.objects.get(id=procurement_id)
        self.assertEqual(procurement.status, ProcurementStatus.POSTED)
        self.assertEqual(procurement.net_kg, Decimal("700.000"))
        self.assertEqual(procurement.total_npr, Decimal("910000.00"))
        self.assertEqual(Lot.objects.get(id=lot_response.data["data"]["id"]).status, LotStatus.QUALITY_PENDING)

    def test_posted_procurement_cannot_be_edited(self):
        self.client.force_authenticate(self.admin)
        farmer = Farmer.objects.create(code="FARM-2026-000001", farmer_name="Sita", phone="9811111111", village="Resunga", district="Gulmi")
        lot = Lot.objects.create(code="LOT-2026-000001", farmer=farmer, item_type="parchment", harvest_year=2026)
        procurement = ProcurementReceipt.objects.create(code="PROC-2026-000001", lot=lot, farmer=farmer, item_type="parchment", gross_kg="10.000", tare_kg="1.000", rate_npr="100.00", status=ProcurementStatus.POSTED)

        response = self.client.patch(f"/api/v1/procurements/{procurement.id}", {"gross_kg": "12.000"}, format="json")
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data["error"]["code"], "POSTED_RECORD_LOCKED")

    def test_viewer_cannot_see_procurement_rate_or_total(self):
        farmer = Farmer.objects.create(code="FARM-2026-000001", farmer_name="Sita", phone="9811111111", village="Resunga", district="Gulmi")
        lot = Lot.objects.create(code="LOT-2026-000001", farmer=farmer, item_type="parchment", harvest_year=2026)
        ProcurementReceipt.objects.create(code="PROC-2026-000001", lot=lot, farmer=farmer, item_type="parchment", gross_kg="10.000", tare_kg="1.000", rate_npr="100.00")

        self.client.force_authenticate(self.viewer)
        response = self.client.get("/api/v1/procurements")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data["data"][0]["rate_npr"])
        self.assertIsNone(response.data["data"][0]["total_npr"])
