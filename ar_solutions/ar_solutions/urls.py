from django.urls import path, include
from landingpage import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', include('custom_admin.urls')),
    path('', views.home, name='home'), # হোম পেজে সব প্রোডাক্ট থাকবে
    path('order/create/', views.create_order, name='create_order'),
    path('order/checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),
    path('<slug:slug>/', views.product_landing, name='product_landing'), # এটি অবশ্যই শেষে থাকবে
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)