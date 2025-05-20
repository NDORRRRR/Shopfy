from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/add/', views.add_product, name='add_product'),  # Tempatkan sebelum pattern dengan parameter dinamis
    path('category/<slug:category_slug>/', views.product_list, name='category_detail'),
    path('product/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]