from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('methods/', views.shipping_methods, name='shipping_methods'),
    path('shipment/<int:order_id>/', views.shipment_detail, name='shipment_detail'),
    path('track/<str:tracking_number>/', views.shipment_track, name='shipment_track'),
]