from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product
from .forms import ProductForm
from django.contrib import messages

def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)[:8]  # Display 8 products on home page
    return render(request, 'products/home.html', {
        'categories': categories,
        'products': products
    })

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)[:4]
    
    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })

@login_required
def add_product(request):
    # Tambahkan debug untuk kategori
    categories = Category.objects.all()
    print(f"Available categories: {list(categories.values('id', 'name', 'slug'))}")
    
    if request.method == 'POST':
        print(f"POST data: {request.POST}")
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produk {product.name} berhasil ditambahkan.')
            return redirect('products:product_detail', id=product.id, slug=product.slug)
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Terjadi kesalahan. Silakan periksa form.')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {
        'form': form,
        'categories': categories,
        'title': 'Tambahkan Product'
    })