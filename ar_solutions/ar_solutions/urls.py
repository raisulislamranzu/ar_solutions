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
    path('page/<slug:slug>/', views.single_page_detail, name='single_page_detail'),
    path('page/<slug:slug>/order/', views.single_page_order, name='single_page_order'),
    path('<slug:slug>/', views.dynamic_landing_dispatcher, name='product_landing'), # dynamic router (SinglePage -> Product)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)