from django.shortcuts import render, redirect
from django.contrib import messages

def about_us(request):
    """View untuk halaman Tentang Kami"""
    return render(request, 'pages/about.html')

def contact(request):
    """View untuk halaman Kontak"""
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        # Simpan pesan atau kirim email (opsional)
        from .models import Contact
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Pesan Anda telah dikirim. Kami akan segera menghubungi Anda.')
        return redirect('contact')  # Change this to the correct URL name
    
    return render(request, 'pages/contact.html')