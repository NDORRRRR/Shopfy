from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ShippingMethod, ShippingZone, ShippingRate, Shipment
from transactions.models import Order

@login_required
def shipping_methods(request):
    shipping_methods = ShippingMethod.objects.filter(active=True)
    return render(request, 'shipping/shipping_methods.html', {
        'shipping_methods': shipping_methods
    })

@login_required
def shipment_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        shipment = order.shipment
    except Shipment.DoesNotExist:
        shipment = None
    
    return render(request, 'shipping/shipment_detail.html', {
        'order': order,
        'shipment': shipment
    })

@login_required
def shipment_track(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number, order__user=request.user)
    
    # Here you would typically integrate with a shipping API to get real-time tracking data
    # For simplicity, we'll just show the current status
    
    return render(request, 'shipping/shipment_track.html', {
        'shipment': shipment
    })