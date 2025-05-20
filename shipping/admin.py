from django.contrib import admin
from .models import ShippingMethod, ShippingZone, ShippingRate, Shipment

@admin.register(ShippingMethod)
class ShippingMethodAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'estimated_days', 'active']
    list_filter = ['active', 'estimated_days']
    search_fields = ['name', 'description']

@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'provinces']
    search_fields = ['name', 'provinces']

class ShippingRateInline(admin.TabularInline):
    model = ShippingRate
    extra = 1

@admin.register(ShippingRate)
class ShippingRateAdmin(admin.ModelAdmin):
    list_display = ['shipping_method', 'shipping_zone', 'price']
    list_filter = ['shipping_method', 'shipping_zone']
    search_fields = ['shipping_method__name', 'shipping_zone__name']

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'shipping_method', 'tracking_number', 'status', 'created_at']
    list_filter = ['status', 'shipping_method', 'created_at']
    search_fields = ['order__id', 'tracking_number', 'notes']
    raw_id_fields = ['order', 'shipping_method']