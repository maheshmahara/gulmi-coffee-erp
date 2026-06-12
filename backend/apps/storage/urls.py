from django.urls import path

from .views import StorageLocationDetailView, StorageLocationListCreateView


urlpatterns = [
    path("storage-locations", StorageLocationListCreateView.as_view(), name="storage-locations"),
    path("storage-locations/", StorageLocationListCreateView.as_view(), name="storage-locations-slash"),
    path("storage-locations/<uuid:location_id>", StorageLocationDetailView.as_view(), name="storage-location-detail"),
    path("storage-locations/<uuid:location_id>/", StorageLocationDetailView.as_view(), name="storage-location-detail-slash"),
]
