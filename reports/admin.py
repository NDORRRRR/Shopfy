from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'generated_by', 'created_at']
    list_filter = ['report_type', 'created_at']
    search_fields = ['title', 'description', 'generated_by__username']
    readonly_fields = ['created_at', 'generated_by', 'parameters']