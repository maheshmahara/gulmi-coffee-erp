from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrManager
from apps.audit.models import AuditAction
from apps.audit.services import AuditService
from apps.common.services import CodeGeneratorService

from .models import Farmer, Lot, ProcurementReceipt, ProcurementStatus
from .serializers import FarmerSerializer, LotSerializer, ProcurementReceiptSerializer
from .services import ProcurementPostingService


def denied(message: str) -> Response:
    return Response({"error": {"code": "PERMISSION_DENIED", "message": message}}, status=status.HTTP_403_FORBIDDEN)


class FarmerListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        farmers = Farmer.objects.order_by("code")
        search = request.query_params.get("search")
        village = request.query_params.get("village")
        district = request.query_params.get("district")
        farmer_type = request.query_params.get("farmer_type")
        active = request.query_params.get("active")
        if search:
            farmers = farmers.filter(Q(code__icontains=search) | Q(farmer_name__icontains=search) | Q(phone__icontains=search) | Q(village__icontains=search))
        if village:
            farmers = farmers.filter(village__icontains=village)
        if district:
            farmers = farmers.filter(district__icontains=district)
        if farmer_type:
            farmers = farmers.filter(farmer_type=farmer_type)
        if active in {"true", "false"}:
            farmers = farmers.filter(active=(active == "true"))
        return Response({"data": FarmerSerializer(farmers, many=True).data, "meta": {"total": farmers.count()}})

    @transaction.atomic
    def post(self, request):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can create farmers.")
        serializer = FarmerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        farmer = serializer.save(
            code=CodeGeneratorService().next_for_model(model=Farmer, prefix="FARM"),
            created_by=request.user,
            updated_by=request.user,
        )
        AuditService().record(action=AuditAction.CREATE, table_name="farmer", actor=request.user, record_id=farmer.id, record_code=farmer.code, new_value=FarmerSerializer(farmer).data)
        return Response({"data": FarmerSerializer(farmer).data, "meta": {}}, status=status.HTTP_201_CREATED)


class FarmerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, farmer_id):
        farmer = get_object_or_404(Farmer, id=farmer_id)
        lots = Lot.objects.filter(farmer=farmer).order_by("-created_at")[:10]
        procurements = ProcurementReceipt.objects.select_related("lot", "farmer", "received_by", "posted_by").filter(farmer=farmer).order_by("-received_at")[:10]
        return Response(
            {
                "data": {
                    **FarmerSerializer(farmer).data,
                    "recent_lots": LotSerializer(lots, many=True).data,
                    "recent_procurements": ProcurementReceiptSerializer(procurements, many=True, context={"role": request.user.role}).data,
                },
                "meta": {},
            }
        )

    def patch(self, request, farmer_id):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can update farmers.")
        farmer = get_object_or_404(Farmer, id=farmer_id)
        old_value = FarmerSerializer(farmer).data
        serializer = FarmerSerializer(farmer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        farmer = serializer.save(updated_by=request.user)
        AuditService().record(action=AuditAction.UPDATE_DRAFT, table_name="farmer", actor=request.user, record_id=farmer.id, record_code=farmer.code, old_value=old_value, new_value=FarmerSerializer(farmer).data)
        return Response({"data": FarmerSerializer(farmer).data, "meta": {}})


class LotListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lots = Lot.objects.select_related("farmer").order_by("-created_at")
        farmer_id = request.query_params.get("farmer_id")
        item_type = request.query_params.get("item_type")
        lot_status = request.query_params.get("status")
        harvest_year = request.query_params.get("harvest_year")
        search = request.query_params.get("search")
        if farmer_id:
            lots = lots.filter(farmer_id=farmer_id)
        if item_type:
            lots = lots.filter(item_type=item_type)
        if lot_status:
            lots = lots.filter(status=lot_status)
        if harvest_year:
            lots = lots.filter(harvest_year=harvest_year)
        if search:
            lots = lots.filter(Q(code__icontains=search) | Q(farmer__farmer_name__icontains=search))
        return Response({"data": LotSerializer(lots, many=True).data, "meta": {"total": lots.count()}})

    @transaction.atomic
    def post(self, request):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can create lots.")
        serializer = LotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lot = serializer.save(
            code=CodeGeneratorService().next_for_model(model=Lot, prefix="LOT"),
            created_by=request.user,
            updated_by=request.user,
        )
        AuditService().record(action=AuditAction.CREATE, table_name="lot", actor=request.user, record_id=lot.id, record_code=lot.code, new_value=LotSerializer(lot).data)
        return Response({"data": LotSerializer(lot).data, "meta": {}}, status=status.HTTP_201_CREATED)


class LotDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lot_id):
        lot = get_object_or_404(Lot.objects.select_related("farmer"), id=lot_id)
        procurements = ProcurementReceipt.objects.select_related("lot", "farmer", "received_by", "posted_by").filter(lot=lot).order_by("-received_at")
        return Response(
            {
                "data": {
                    **LotSerializer(lot).data,
                    "procurements": ProcurementReceiptSerializer(procurements, many=True, context={"role": request.user.role}).data,
                },
                "meta": {},
            }
        )

    def patch(self, request, lot_id):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can update lots.")
        lot = get_object_or_404(Lot, id=lot_id)
        old_value = LotSerializer(lot).data
        serializer = LotSerializer(lot, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        lot = serializer.save(updated_by=request.user)
        AuditService().record(action=AuditAction.UPDATE_DRAFT, table_name="lot", actor=request.user, record_id=lot.id, record_code=lot.code, old_value=old_value, new_value=LotSerializer(lot).data)
        return Response({"data": LotSerializer(lot).data, "meta": {}})


class ProcurementListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        procurements = ProcurementReceipt.objects.select_related("lot", "farmer", "received_by", "posted_by").order_by("-received_at")
        farmer_id = request.query_params.get("farmer_id")
        lot_id = request.query_params.get("lot_id")
        item_type = request.query_params.get("item_type")
        procurement_status = request.query_params.get("status")
        received_from = request.query_params.get("received_from")
        received_to = request.query_params.get("received_to")
        if farmer_id:
            procurements = procurements.filter(farmer_id=farmer_id)
        if lot_id:
            procurements = procurements.filter(lot_id=lot_id)
        if item_type:
            procurements = procurements.filter(item_type=item_type)
        if procurement_status:
            procurements = procurements.filter(status=procurement_status)
        if received_from:
            procurements = procurements.filter(received_at__gte=received_from)
        if received_to:
            procurements = procurements.filter(received_at__lte=received_to)
        serializer = ProcurementReceiptSerializer(procurements, many=True, context={"role": request.user.role})
        return Response({"data": serializer.data, "meta": {"total": procurements.count()}})

    @transaction.atomic
    def post(self, request):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can create procurements.")
        serializer = ProcurementReceiptSerializer(data=request.data, context={"role": request.user.role})
        serializer.is_valid(raise_exception=True)
        procurement = serializer.save(
            code=CodeGeneratorService().next_for_model(model=ProcurementReceipt, prefix="PROC"),
            received_by=serializer.validated_data.get("received_by") or request.user,
            created_by=request.user,
            updated_by=request.user,
        )
        AuditService().record(action=AuditAction.CREATE, table_name="procurement_receipt", actor=request.user, record_id=procurement.id, record_code=procurement.code, new_value=ProcurementReceiptSerializer(procurement, context={"role": "admin"}).data)
        return Response({"data": ProcurementReceiptSerializer(procurement, context={"role": request.user.role}).data, "meta": {}}, status=status.HTTP_201_CREATED)


class ProcurementDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, procurement_id):
        procurement = get_object_or_404(ProcurementReceipt.objects.select_related("lot", "farmer", "received_by", "posted_by"), id=procurement_id)
        return Response({"data": ProcurementReceiptSerializer(procurement, context={"role": request.user.role}).data, "meta": {}})

    def patch(self, request, procurement_id):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can update procurements.")
        procurement = get_object_or_404(ProcurementReceipt.objects.select_related("lot", "farmer", "received_by", "posted_by"), id=procurement_id)
        if procurement.status != ProcurementStatus.DRAFT:
            return Response({"error": {"code": "POSTED_RECORD_LOCKED", "message": "Posted procurement cannot be edited."}}, status=status.HTTP_409_CONFLICT)
        old_value = ProcurementReceiptSerializer(procurement, context={"role": "admin"}).data
        serializer = ProcurementReceiptSerializer(procurement, data=request.data, partial=True, context={"role": request.user.role})
        serializer.is_valid(raise_exception=True)
        procurement = serializer.save(updated_by=request.user)
        AuditService().record(action=AuditAction.UPDATE_DRAFT, table_name="procurement_receipt", actor=request.user, record_id=procurement.id, record_code=procurement.code, old_value=old_value, new_value=ProcurementReceiptSerializer(procurement, context={"role": "admin"}).data)
        return Response({"data": ProcurementReceiptSerializer(procurement, context={"role": request.user.role}).data, "meta": {}})


class ProcurementPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, procurement_id):
        if not IsAdminOrManager().has_permission(request, self):
            return denied("Only Admin and Manager can post procurements.")
        procurement = get_object_or_404(ProcurementReceipt, id=procurement_id)
        try:
            procurement = ProcurementPostingService().post(procurement=procurement, actor=request.user)
        except ValueError as exc:
            if str(exc) == "POSTED_RECORD_LOCKED":
                return Response({"error": {"code": "POSTED_RECORD_LOCKED", "message": "Posted procurement cannot be edited."}}, status=status.HTTP_409_CONFLICT)
            return Response({"error": {"code": str(exc), "message": "Procurement failed validation."}}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": ProcurementReceiptSerializer(procurement, context={"role": request.user.role}).data, "meta": {}})
