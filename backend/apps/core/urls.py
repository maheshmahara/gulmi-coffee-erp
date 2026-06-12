from django.urls import path
from django.urls import include

from .views import health


urlpatterns = [
    path("", include("apps.accounts.urls")),
    path("", include("apps.procurement.urls")),
    path("", include("apps.storage.urls")),
    path("health", health, name="health"),
    path("health/", health, name="health-slash"),
]
