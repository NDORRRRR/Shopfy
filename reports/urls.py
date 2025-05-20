from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('sales/', views.sales_report, name='sales_report'),
    path('customers/', views.customer_report, name='customer_report'),
    path('export/sales/<int:report_id>/', views.export_sales_csv, name='export_sales_csv'),
    path('products/', views.product_report, name='product_report'),
]