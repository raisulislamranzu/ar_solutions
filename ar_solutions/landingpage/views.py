import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import messages

from .models import SiteSetting, Product, Order, Category, SinglePage, SinglePageBundle

def _build_products_data(products):
    """Serialize active products into plain dicts for the store-front JavaScript."""
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'title': p.title,
            'slug': p.slug,
            'category': p.category.name if p.category else '',
            'price': float(p.discount_price) if p.discount_price else 0.0,
            'oldPrice': float(p.regular_price) if p.regular_price else 0.0,
            'image': p.image.url if p.image else '',
            'description': p.description,
            'rating': float(p.rating),
            'reviewsCount': p.reviews_count,
            'highlights': p.highlight_list,
            'badge': p.badge,
            'discountPercent': p.discount_percent,
            'deliveryInside': p.delivery_inside_dhaka,
            'deliveryOutside': p.delivery_outside_dhaka,
        })
    return data


@ensure_csrf_cookie
def home(request):
    site_setting = SiteSetting.objects.first()
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    context = {
        'site': site_setting,
        'products': products,
        'categories': categories,
        'products_data': _build_products_data(products),
    }
    return render(request, 'landingpage/home.html', context)

def single_page_detail(request, slug):
    site_setting = SiteSetting.objects.first()
    page = get_object_or_404(SinglePage.objects.prefetch_related('bundles'), slug=slug, is_active=True)
    return render(request, 'landingpage/single_page.html', {
        'site': site_setting,
        'page': page,
    })


@require_POST
def single_page_order(request, slug):
    page = get_object_or_404(SinglePage, slug=slug, is_active=True)
    
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)
        name = (data.get('customer_name') or '').strip()
        phone = (data.get('phone_number') or '').strip()
        address = (data.get('address') or '').strip()
        area = data.get('delivery_area') or 'Inside Dhaka'
        bundle_id = data.get('bundle_id')
    else:
        name = (request.POST.get('customer_name') or '').strip()
        phone = (request.POST.get('phone_number') or '').strip()
        address = (request.POST.get('address') or '').strip()
        area = request.POST.get('delivery_area') or 'Inside Dhaka'
        bundle_id = request.POST.get('bundle_id')

    if not (name and phone and address):
        if request.content_type == 'application/json':
            return JsonResponse({'success': False, 'message': 'অনুগ্রহ করে সব তথ্য সঠিকভাবে পূরণ করুন।'}, status=400)
        messages.error(request, 'অনুগ্রহ করে সব তথ্য সঠিকভাবে পূরণ করুন।')
        return redirect('single_page_detail', slug=slug)

    # Determine bundle / package pricing
    package_name = page.title
    quantity = 1
    sub_total = page.discount_price

    if bundle_id and str(bundle_id) != 'default':
        try:
            bundle = page.bundles.get(pk=bundle_id)
            package_name = bundle.name
            sub_total = bundle.price
            quantity = bundle.quantity
        except (SinglePageBundle.DoesNotExist, ValueError):
            pass

    # Delivery charge
    if area == 'Outside Dhaka':
        delivery_charge = page.delivery_outside_dhaka
    else:
        delivery_charge = page.delivery_inside_dhaka

    total_bill = sub_total + delivery_charge

    order = Order.objects.create(
        product=page.linked_product,
        landing_page=page,
        package_name=package_name,
        customer_name=name,
        phone_number=phone,
        address=address,
        delivery_area=area,
        quantity=quantity,
        sub_total=sub_total,
        delivery_charge=delivery_charge,
        total_bill=total_bill,
        status='Pending'
    )

    if request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'redirect_url': '/success/'
        })

    return redirect('success')


def dynamic_landing_dispatcher(request, slug):
    """
    Intelligent slug router:
    1. If a SinglePage with this slug exists and is active, render or order the custom single page.
    2. Else if a Product with this slug exists and is active, render product_landing.
    3. Else 404.
    """
    single_page = SinglePage.objects.filter(slug=slug, is_active=True).prefetch_related('bundles').first()
    if single_page:
        if request.method == 'POST':
            return single_page_order(request, slug)
        site_setting = SiteSetting.objects.first()
        return render(request, 'landingpage/single_page.html', {
            'site': site_setting,
            'page': single_page,
        })
    return product_landing(request, slug)


# নির্দিষ্ট প্রোডাক্টের ল্যান্ডিং পেজ
def product_landing(request, slug):
    site_setting = SiteSetting.objects.first()
    product = get_object_or_404(Product, slug=slug, is_active=True)

    if request.method == "POST":
        name = (request.POST.get('name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        address = (request.POST.get('address') or '').strip()
        area = request.POST.get('area') or 'Inside Dhaka'
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
        if quantity < 1:
            quantity = 1

        if not (name and phone and address):
            messages.error(request, 'অনুগ্রহ করে আপনার নাম, মোবাইল নাম্বার এবং সম্পূর্ণ ঠিকানা সঠিকভাবে পূরণ করুন।')
            return render(request, 'landingpage/index.html', {'site': site_setting, 'product': product})

        delivery_charge = product.delivery_inside_dhaka if area == 'Inside Dhaka' else product.delivery_outside_dhaka
        sub_total = product.discount_price * quantity
        total_bill = sub_total + delivery_charge

        Order.objects.create(
            product=product,
            package_name=product.title,
            customer_name=name,
            phone_number=phone,
            address=address,
            delivery_area=area,
            quantity=quantity,
            sub_total=sub_total,
            delivery_charge=delivery_charge,
            total_bill=total_bill,
            status='Pending'
        )
        return redirect('success')

    context = {
        'site': site_setting,
        'product': product,
    }
    return render(request, 'landingpage/index.html', context)


def success(request):
    site_setting = SiteSetting.objects.first()
    return render(request, 'landingpage/success.html', {'site': site_setting})


# ---------------------------------------------------------------------------
# AJAX order endpoints (used by the store-front Quick Order modal & cart)
# ---------------------------------------------------------------------------
def _delivery_charge(product, area):
    if area == 'Outside Dhaka':
        return product.delivery_outside_dhaka
    return product.delivery_inside_dhaka


@require_POST
def create_order(request):
    """Create a single order from the Quick Order modal."""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

    product_id = payload.get('product_id')
    name = (payload.get('name') or '').strip()
    phone = (payload.get('phone') or '').strip()
    address = (payload.get('address') or '').strip()
    area = payload.get('area') or 'Inside Dhaka'
    try:
        quantity = int(payload.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1
    if quantity < 1:
        quantity = 1

    if not (name and phone and address):
        return JsonResponse({'success': False, 'message': 'অনুগ্রহ করে সব তথ্য পূরণ করুন।'}, status=400)

    product = get_object_or_404(Product, pk=product_id, is_active=True)

    delivery_charge = _delivery_charge(product, area)
    sub_total = product.discount_price * quantity
    total_bill = sub_total + delivery_charge

    order = Order.objects.create(
        product=product,
        package_name=product.title,
        customer_name=name,
        phone_number=phone,
        address=address,
        delivery_area=area,
        quantity=quantity,
        sub_total=sub_total,
        delivery_charge=delivery_charge,
        total_bill=total_bill,
        status='Pending',
    )
    return JsonResponse({'success': True, 'order_id': order.id,
                         'message': 'আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।'})


@require_POST
def checkout(request):
    """Create one order per cart line item from the cart checkout modal."""
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'success': False, 'message': 'Invalid request.'}, status=400)

    name = (payload.get('name') or '').strip()
    phone = (payload.get('phone') or '').strip()
    address = (payload.get('address') or '').strip()
    area = payload.get('area') or 'Inside Dhaka'
    items = payload.get('items') or []

    if not (name and phone and address):
        return JsonResponse({'success': False, 'message': 'অনুগ্রহ করে সব তথ্য পূরণ করুন।'}, status=400)
    if not items:
        return JsonResponse({'success': False, 'message': 'আপনার কার্ট খালি।'}, status=400)

    created_ids = []
    for item in items:
        try:
            product = Product.objects.get(pk=item.get('product_id'), is_active=True)
        except (Product.DoesNotExist, ValueError, TypeError):
            continue
        try:
            quantity = int(item.get('quantity', 1))
        except (TypeError, ValueError):
            quantity = 1
        if quantity < 1:
            quantity = 1

        delivery_charge = _delivery_charge(product, area)
        sub_total = product.discount_price * quantity
        total_bill = sub_total + delivery_charge
        order = Order.objects.create(
            product=product,
            package_name=product.title,
            customer_name=name,
            phone_number=phone,
            address=address,
            delivery_area=area,
            quantity=quantity,
            sub_total=sub_total,
            delivery_charge=delivery_charge,
            total_bill=total_bill,
            status='Pending',
        )
        created_ids.append(order.id)

    if not created_ids:
        return JsonResponse({'success': False, 'message': 'কোনো বৈধ পণ্য পাওয়া যায়নি।'}, status=400)

    return JsonResponse({'success': True, 'order_ids': created_ids,
                         'message': 'আপনার অর্ডারটি সফলভাবে গ্রহণ করা হয়েছে।'})