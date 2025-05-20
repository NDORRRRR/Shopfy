from django.urls import path
from . import views

urlpatterns = [
    path('tentang-kami/', views.about_us, name='about_us'),
    path('kontak/', views.contact, name='contact'),
]