from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home
from pages.views import about_us, contact  # Impor view functions dari pages/views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('products/', include('products.urls', namespace='products')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
    path('shipping/', include('shipping.urls', namespace='shipping')),
    path('reports/', include('reports.urls', namespace='reports')),
    path('', home, name='home'),  # Home page
    path('tentang-kami/', about_us, name='about_us'),  # About Us page
    path('kontak/', contact, name='contact'),  # Contact page
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)