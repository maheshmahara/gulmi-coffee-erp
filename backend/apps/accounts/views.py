from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.models import AuditAction
from apps.audit.services import AuditService
from apps.common.services import CodeGeneratorService

from .permissions import IsAdmin
from .serializers import CurrentUserSerializer, UserCreateSerializer, UserListSerializer, UserUpdateSerializer


AppUser = get_user_model()


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        identifier = request.data.get("phone") or request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=identifier, password=password)
        if user is None and identifier:
            try:
                candidate = AppUser.objects.get(phone=identifier)
                user = authenticate(request, username=candidate.username, password=password)
            except AppUser.DoesNotExist:
                user = None

        if user is None:
            return Response({"error": {"code": "AUTH_REQUIRED", "message": "Invalid credentials."}}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.active:
            return Response({"error": {"code": "PERMISSION_DENIED", "message": "This user is inactive."}}, status=status.HTTP_403_FORBIDDEN)

        login(request, user)
        AuditService().record(action=AuditAction.LOGIN, table_name="app_user", actor=user, record_id=user.id, record_code=user.code or user.username)
        return Response({"data": {"user": CurrentUserSerializer(user).data}, "meta": {}})


@method_decorator(csrf_exempt, name="dispatch")
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        AuditService().record(action=AuditAction.LOGOUT, table_name="app_user", actor=user, record_id=user.id, record_code=user.code or user.username)
        logout(request)
        return Response({"data": {"status": "logged_out"}, "meta": {}})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    return Response({"data": CurrentUserSerializer(request.user).data, "meta": {}})


class UserListCreateView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        users = AppUser.objects.order_by("created_at")
        return Response({"data": UserListSerializer(users, many=True).data, "meta": {"total": users.count()}})

    @transaction.atomic
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if not user.code:
            user.code = CodeGeneratorService().next_for_model(model=AppUser, prefix="USER")
            user.save(update_fields=["code"])
        AuditService().record(action=AuditAction.CREATE, table_name="app_user", actor=request.user, record_id=user.id, record_code=user.code, new_value=UserListSerializer(user).data)
        return Response({"data": UserListSerializer(user).data, "meta": {}}, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    permission_classes = [IsAdmin]

    def get_object(self, user_id):
        return AppUser.objects.get(id=user_id)

    def get(self, request, user_id):
        return Response({"data": UserListSerializer(self.get_object(user_id)).data, "meta": {}})

    def patch(self, request, user_id):
        user = self.get_object(user_id)
        old_value = UserListSerializer(user).data
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        AuditService().record(action=AuditAction.UPDATE_DRAFT, table_name="app_user", actor=request.user, record_id=user.id, record_code=user.code, old_value=old_value, new_value=UserListSerializer(user).data)
        return Response({"data": UserListSerializer(user).data, "meta": {}})
