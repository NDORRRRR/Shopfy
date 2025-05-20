from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import redirect
from .forms import SignUpForm, LoginForm, CustomerProfileForm, UserUpdateForm
from .models import Address

def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.success(request, 'Akun berhasil dibuat! Silahkan lengkapi profil Anda.')
            return redirect('accounts:profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('products:home')
        
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Anda berhasil login sebagai {username}.")
                return redirect('products:home')
            else:
                messages.error(request, "Username atau password salah.")
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Anda berhasil logout.")
    return redirect('accounts:login')

@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = CustomerProfileForm(request.POST, request.FILES, instance=request.user.customer)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = CustomerProfileForm(instance=request.user.customer)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile.html', context)

@login_required
@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        
        # Update customer profile
        customer = user.customer
        customer.phone_number = request.POST.get('phone', '')
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            # Hapus foto lama jika ada
            if customer.profile_picture:
                import os
                if os.path.isfile(customer.profile_picture.path):
                    os.remove(customer.profile_picture.path)
            
            customer.profile_picture = request.FILES['profile_picture']
        
        customer.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')

@login_required
def add_address(request):
    if request.method == 'POST':
        # Process the form data
        # Assuming you have an Address model associated with the user
        address = Address(
            user=request.user,
            recipient_name=request.POST.get('recipient_name', ''),
            phone_number=request.POST.get('phone_number', ''),
            street_address=request.POST.get('street_address', ''),
            city=request.POST.get('city', ''),
            province=request.POST.get('province', ''),
            postal_code=request.POST.get('postal_code', ''),
            is_default=request.POST.get('is_default') == 'on'  # Checkbox handling
        )
        address.save()
        
        # If this is set as default, unset other defaults
        if address.is_default:
            Address.objects.filter(user=request.user).exclude(id=address.id).update(is_default=False)
            
        messages.success(request, 'Alamat baru berhasil ditambahkan!')
        return redirect('accounts:profile')
    
    # If GET request, render form
    return render(request, 'accounts/add_address.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        # Django provides a built-in form for password changes
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Important: update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Kata sandi Anda berhasil diubah!')
            return redirect('accounts:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    
    return redirect('accounts:profile')

@login_required
def update_notifications(request):
    if request.method == 'POST':
        profile = request.user.profile

        profile.notify_promos = request.POST.get('email_promo') == 'on'
        profile.notify_orders = request.POST.get('email_order') == 'on'
        profile.notify_news = request.POST.get('email_news') == 'on'
        profile.save()
        
        messages.success(request, 'Pengaturan notifikasi berhasil diperbarui!')
        return redirect('accounts:profile')
    
    return redirect('accounts:profile')

from django.shortcuts import get_object_or_404

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alamat berhasil diperbarui')
            return redirect('accounts:profile')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'accounts/edit_address.html', {'form': form, 'address': address})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    
    if request.method == 'POST':
        # Jika alamat yang dihapus adalah alamat default, atur alamat lain sebagai default
        if address.is_default:
            other_address = Address.objects.filter(user=request.user).exclude(id=address_id).first()
            if other_address:
                other_address.is_default = True
                other_address.save()
        
        address.delete()
        messages.success(request, 'Alamat berhasil dihapus')
    
    return redirect('accounts:profile')

@login_required
def set_default_address(request, address_id):
    if request.method == 'POST':
        # Hapus status default dari semua alamat pengguna
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # Set alamat yang dipilih sebagai default
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.is_default = True
        address.save()
        
        messages.success(request, 'Alamat utama berhasil diubah')
    
    return redirect('accounts:profile')

def set_default_address(request, address_id):
    if request.method == 'POST':
        # Hapus status default dari semua alamat pengguna
        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        
        # Set alamat yang dipilih sebagai default
        address = get_object_or_404(Address, id=address_id, user=request.user)
        address.is_default = True
        address.save()
        
        messages.success(request, 'Alamat utama berhasil diubah')
    
    return redirect('accounts:profile')