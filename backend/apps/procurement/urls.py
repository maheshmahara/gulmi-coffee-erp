from django.urls import path

from .views import (
    FarmerDetailView,
    FarmerListCreateView,
    LotDetailView,
    LotListCreateView,
    ProcurementDetailView,
    ProcurementListCreateView,
    ProcurementPostView,
)

urlpatterns = [
    path("farmers", FarmerListCreateView.as_view(), name="farmers"),
    path("farmers/<uuid:farmer_id>", FarmerDetailView.as_view(), name="farmer-detail"),
    path("lots", LotListCreateView.as_view(), name="lots"),
    path("lots/<uuid:lot_id>", LotDetailView.as_view(), name="lot-detail"),
    path("procurements", ProcurementListCreateView.as_view(), name="procurements"),
    path("procurements/<uuid:procurement_id>", ProcurementDetailView.as_view(), name="procurement-detail"),
    path("procurements/<uuid:procurement_id>/post", ProcurementPostView.as_view(), name="procurement-post"),
]
