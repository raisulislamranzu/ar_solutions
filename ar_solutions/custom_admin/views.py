from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate

from landingpage.models import Product, Category, Order, SiteSetting
from .forms import ProductForm, CategoryForm, OrderForm, SiteSettingForm


# Only staff users are allowed into the custom admin panel.
def is_staff_user(user):
    return user.is_active and user.is_staff


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def dashboard(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_revenue = Order.objects.filter(status='Completed').aggregate(Sum('total_bill'))['total_bill__sum'] or 0

    recent_orders = Order.objects.select_related('product').order_by('-created_at')[:8]
    orders_by_status = Order.objects.values('status').annotate(count=Count('id')).order_by('status')

    daily_sales = (
        Order.objects.filter(status='Completed')
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Sum('total_bill'))
        .order_by('-day')[:7]
    )

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'orders_by_status': orders_by_status,
        'daily_sales': list(reversed(list(daily_sales))),
    }
    return render(request, 'custom_admin/dashboard.html', context)


# ---------------------------------------------------------------------------
# Product CRUD
# ---------------------------------------------------------------------------
@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def product_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.select_related('category').all()
    if query:
        products = products.filter(title__icontains=query)
    return render(request, 'custom_admin/product_list.html', {'products': products, 'query': query})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('custom_admin:product_list')
    else:
        form = ProductForm()
    return render(request, 'custom_admin/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('custom_admin:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'custom_admin/product_form.html', {'form': form, 'title': 'Edit Product'})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('custom_admin:product_list')
    return render(request, 'custom_admin/product_confirm_delete.html', {'object': product, 'type': 'Product'})


# ---------------------------------------------------------------------------
# Category CRUD
# ---------------------------------------------------------------------------
@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def category_list(request):
    query = request.GET.get('q', '')
    categories = Category.objects.annotate(product_count=Count('products')).all()
    if query:
        categories = categories.filter(name__icontains=query)
    return render(request, 'custom_admin/category_list.html', {'categories': categories, 'query': query})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('custom_admin:category_list')
    else:
        form = CategoryForm()
    return render(request, 'custom_admin/category_form.html', {'form': form, 'title': 'Add Category'})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('custom_admin:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'custom_admin/category_form.html', {'form': form, 'title': 'Edit Category'})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('custom_admin:category_list')
    return render(request, 'custom_admin/category_confirm_delete.html', {'object': category, 'type': 'Category'})


# ---------------------------------------------------------------------------
# Order management
# ---------------------------------------------------------------------------
@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def order_list(request):
    status = request.GET.get('status', '')
    query = request.GET.get('q', '')
    orders = Order.objects.select_related('product').all()
    if status:
        orders = orders.filter(status=status)
    if query:
        orders = orders.filter(customer_name__icontains=query) | orders.filter(phone_number__icontains=query)
    return render(request, 'custom_admin/order_list.html', {
        'orders': orders,
        'status': status,
        'query': query,
        'status_choices': Order.STATUS_CHOICES,
    })


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('product'), pk=pk)
    return render(request, 'custom_admin/order_detail.html', {'order': order})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully.')
            return redirect('custom_admin:order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'custom_admin/order_form.html', {'form': form, 'title': f'Edit Order #{order.pk}'})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Order deleted successfully.')
        return redirect('custom_admin:order_list')
    return render(request, 'custom_admin/order_confirm_delete.html', {'object': order, 'type': 'Order'})


@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def order_invoice(request, pk):
    order = get_object_or_404(Order, pk=pk)
    site_setting = SiteSetting.objects.first()
    return render(request, 'custom_admin/invoice.html', {'order': order, 'site': site_setting})


# ---------------------------------------------------------------------------
# Site settings (singleton)
# ---------------------------------------------------------------------------
@login_required(login_url='custom_admin:login')
@user_passes_test(is_staff_user, login_url='custom_admin:login')
def site_setting_edit(request):
    setting = SiteSetting.objects.first()
    if setting is None:
        setting = SiteSetting.objects.create()

    if request.method == 'POST':
        form = SiteSettingForm(request.POST, request.FILES, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully.')
            return redirect('custom_admin:site_setting_edit')
    else:
        form = SiteSettingForm(instance=setting)
    return render(request, 'custom_admin/site_setting_form.html', {'form': form})




