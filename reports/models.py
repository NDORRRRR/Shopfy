from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    REPORT_TYPES = (
        ('sales', 'Sales Report'),
        ('customer', 'Customer Report'),
        ('shipping', 'Shipping Report'),
        ('product', 'Product Report'),
    )
    
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    description = models.TextField(blank=True, null=True)
    parameters = models.JSONField(default=dict, blank=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title