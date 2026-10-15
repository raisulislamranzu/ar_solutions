from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'custom_admin'

urlpatterns = [
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='custom_admin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Products CRUD
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Categories CRUD
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('orders/<int:pk>/invoice/', views.order_invoice, name='order_invoice'),

    # Site Settings
    path('settings/', views.site_setting_edit, name='site_setting_edit'),
]
