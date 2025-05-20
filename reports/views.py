from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from django.contrib import messages
from django.http import HttpResponse
import csv
import datetime
from .models import Report
from transactions.models import Order, OrderItem
from accounts.models import Customer
from products.models import Product

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def report_list(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'reports/report_list.html', {'reports': reports})

@user_passes_test(is_admin)
def sales_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            
            orders = Order.objects.filter(
                created_at__date__gte=start_date,
                created_at__date__lte=end_date
            )
            
            total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            
            report = Report.objects.create(
                title=f'Sales Report {start_date} to {end_date}',
                report_type='sales',
                description=f'Sales report from {start_date} to {end_date}',
                parameters={'start_date': str(start_date), 'end_date': str(end_date)},
                generated_by=request.user
            )
            
            context = {
                'orders': orders,
                'start_date': start_date,
                'end_date': end_date,
                'total_sales': total_sales,
                'report': report
            }
            
            return render(request, 'reports/sales_report.html', context)
            
        except (ValueError, TypeError):
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD format.')
    
    return render(request, 'reports/sales_report_form.html')

@user_passes_test(is_admin)
def customer_report(request):
    customers = Customer.objects.all()
    
    for customer in customers:
        customer.order_count = Order.objects.filter(user=customer.user).count()
        customer.total_spent = Order.objects.filter(user=customer.user).aggregate(
            Sum('total_price')
        )['total_price__sum'] or 0
    
    customers = sorted(customers, key=lambda c: c.total_spent, reverse=True)
    
    report = Report.objects.create(
        title='Customer Report',
        report_type='customer',
        description='Customer report with order statistics',
        parameters={},
        generated_by=request.user
    )
    
    context = {
        'customers': customers,
        'report': report
    }
    
    return render(request, 'reports/customer_report.html', context)

@user_passes_test(is_admin)
def export_sales_csv(request, report_id):
    report = get_object_or_404(Report, id=report_id, report_type='sales')
    
    start_date = datetime.datetime.strptime(report.parameters['start_date'], '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(report.parameters['end_date'], '%Y-%m-%d').date()
    
    orders = Order.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    )
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date}_to_{end_date}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Date', 'Customer', 'Items', 'Total Price', 'Status'])
    
    for order in orders:
        writer.writerow([
            order.id,
            order.created_at.strftime('%Y-%m-%d %H:%M'),
            order.user.username,
            ', '.join([f"{item.quantity}x {item.product.name}" for item in order.items.all()]),
            order.total_price,
            order.status
        ])
    
    return response