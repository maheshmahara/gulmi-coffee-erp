from django.contrib import admin

from .models import Farmer, Lot, ProcurementReceipt


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ("code", "farmer_name", "phone", "village", "district", "farmer_type", "active")
    search_fields = ("code", "farmer_name", "phone", "village", "district")
    list_filter = ("farmer_type", "district", "active")


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ("code", "farmer", "item_type", "harvest_year", "status", "created_at")
    search_fields = ("code", "farmer__farmer_name", "farmer__code")
    list_filter = ("item_type", "harvest_year", "status")


@admin.register(ProcurementReceipt)
class ProcurementReceiptAdmin(admin.ModelAdmin):
    list_display = ("code", "lot", "farmer", "item_type", "net_kg", "rate_npr", "total_npr", "status", "received_at")
    search_fields = ("code", "lot__code", "farmer__farmer_name", "farmer__code")
    list_filter = ("item_type", "status", "received_at")
    readonly_fields = ("net_kg", "total_npr", "posted_at", "posted_by")
