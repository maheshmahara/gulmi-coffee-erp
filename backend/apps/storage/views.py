from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdminOrManager
from apps.audit.models import AuditAction
from apps.audit.services import AuditService
from apps.common.services import CodeGeneratorService

from .models import StorageLocation
from .serializers import StorageLocationSerializer


class StorageLocationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        locations = StorageLocation.objects.select_related("parent_location").order_by("code")
        location_type = request.query_params.get("location_type")
        active = request.query_params.get("active")
        search = request.query_params.get("search")
        if location_type:
            locations = locations.filter(location_type=location_type)
        if active in {"true", "false"}:
            locations = locations.filter(active=(active == "true"))
        if search:
            locations = locations.filter(location_name__icontains=search)
        return Response({"data": StorageLocationSerializer(locations, many=True).data, "meta": {"total": locations.count()}})

    @transaction.atomic
    def post(self, request):
        if not IsAdminOrManager().has_permission(request, self):
            return Response({"error": {"code": "PERMISSION_DENIED", "message": "Only Admin and Manager can create storage locations."}}, status=status.HTTP_403_FORBIDDEN)
        serializer = StorageLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        location = serializer.save(
            code=CodeGeneratorService().next_for_model(model=StorageLocation, prefix="LOC"),
            created_by=request.user,
            updated_by=request.user,
        )
        AuditService().record(action=AuditAction.CREATE, table_name="storage_location", actor=request.user, record_id=location.id, record_code=location.code, new_value=StorageLocationSerializer(location).data)
        return Response({"data": StorageLocationSerializer(location).data, "meta": {}}, status=status.HTTP_201_CREATED)


class StorageLocationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, location_id):
        return StorageLocation.objects.get(id=location_id)

    def get(self, request, location_id):
        return Response({"data": StorageLocationSerializer(self.get_object(location_id)).data, "meta": {}})

    def patch(self, request, location_id):
        if not IsAdminOrManager().has_permission(request, self):
            return Response({"error": {"code": "PERMISSION_DENIED", "message": "Only Admin and Manager can update storage locations."}}, status=status.HTTP_403_FORBIDDEN)
        location = self.get_object(location_id)
        old_value = StorageLocationSerializer(location).data
        serializer = StorageLocationSerializer(location, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        location = serializer.save(updated_by=request.user)
        AuditService().record(action=AuditAction.UPDATE_DRAFT, table_name="storage_location", actor=request.user, record_id=location.id, record_code=location.code, old_value=old_value, new_value=StorageLocationSerializer(location).data)
        return Response({"data": StorageLocationSerializer(location).data, "meta": {}})
