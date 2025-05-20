from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from .forms import OrderCreateForm

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product)
    
    messages.success(request, f'{product.name} ditambahkan ke keranjang!')
    return redirect('transactions:cart_detail')

@login_required
def cart_remove(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item dihapus dari keranjang!')
    return redirect('transactions:cart_detail')

@login_required
def cart_update(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        new_quantity = int(request.POST.get('quantity', 1))
        if new_quantity > 0 and new_quantity <= cart_item.product.stock:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, 'Jumlah produk diperbarui!')
        else:
            messages.error(request, 'Jumlah produk tidak valid!')
    except ValueError:
        messages.error(request, 'Jumlah produk tidak valid!')
    
    return redirect('transactions:cart_detail')

@login_required
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    return render(request, 'transactions/cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items
    })

@login_required
def order_create(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.error(request, 'Keranjang Anda kosong!')
            return redirect('transactions:cart_detail')
    except Cart.DoesNotExist:
        messages.error(request, 'Keranjang Anda kosong!')
        return redirect('transactions:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()
            
            # Create order items from cart items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
                
                # Update product stock
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            # Clear the cart
            cart.delete()
            
            return render(request, 'transactions/order_created.html', {'order': order})
    else:
        # Pre-fill form with user profile data if available
        initial_data = {}
        if hasattr(request.user, 'customer'):
            customer = request.user.customer
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'address': customer.address,
                'city': customer.city,
                'province': customer.province,
                'postal_code': customer.postal_code,
                'phone': customer.phone_number
            }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'transactions/order_create.html', {
        'cart': cart,
        'cart_items': cart_items,
        'form': form
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'transactions/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'transactions/order_detail.html', {'order': order})