from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'city', 'province', 'postal_code', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }