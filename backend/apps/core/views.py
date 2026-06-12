from django.conf import settings
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    database_status = "ok"
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        database_status = "unavailable"

    overall = "ok" if database_status == "ok" else "degraded"
    return Response(
        {
            "data": {
                "status": overall,
                "database": database_status,
                "version": settings.APP_VERSION,
                "service": "gulmi-coffee-erp-backend",
            },
            "meta": {},
        }
    )
