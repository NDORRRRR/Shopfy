from django.contrib import admin
from .models import Customer

# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'created_at']
    list_filter = ['city', 'province', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number', 'address', 'city']
    raw_id_fields = ['user']