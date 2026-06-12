from django.db import transaction
from django.utils import timezone

from apps.audit.models import AuditAction
from apps.audit.services import AuditService

from .models import LotStatus, ProcurementReceipt, ProcurementStatus
from .serializers import ProcurementReceiptSerializer


class ProcurementPostingService:
    @transaction.atomic
    def post(self, *, procurement: ProcurementReceipt, actor) -> ProcurementReceipt:
        procurement = ProcurementReceipt.objects.select_for_update().select_related("lot", "farmer").get(id=procurement.id)
        if procurement.status != ProcurementStatus.DRAFT:
            raise ValueError("POSTED_RECORD_LOCKED")
        if procurement.gross_kg <= 0 or procurement.tare_kg < 0 or procurement.gross_kg <= procurement.tare_kg:
            raise ValueError("INVALID_PROCUREMENT_WEIGHT")

        old_value = ProcurementReceiptSerializer(procurement, context={"role": "admin"}).data
        procurement.status = ProcurementStatus.POSTED
        procurement.posted_at = timezone.now()
        procurement.posted_by = actor
        procurement.updated_by = actor
        procurement.save()

        lot = procurement.lot
        lot.status = LotStatus.QUALITY_PENDING
        lot.updated_by = actor
        lot.save(update_fields=["status", "updated_by", "updated_at"])

        AuditService().record(
            action=AuditAction.POST,
            table_name="procurement_receipt",
            actor=actor,
            record_id=procurement.id,
            record_code=procurement.code,
            old_value=old_value,
            new_value=ProcurementReceiptSerializer(procurement, context={"role": "admin"}).data,
        )
        return procurement
