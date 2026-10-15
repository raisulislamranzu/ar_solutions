from django import forms
from landingpage.models import Product, Category, Order, SiteSetting


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Electronics'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. electronics'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'title', 'slug', 'category', 'description',
            'regular_price', 'discount_price', 'image', 'video_url',
            'delivery_inside_dhaka', 'delivery_outside_dhaka',
            'badge', 'rating', 'reviews_count', 'highlights', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'regular_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control'}),
            'delivery_inside_dhaka': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_outside_dhaka': forms.NumberInput(attrs={'class': 'form-control'}),
            'badge': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "e.g. বেস্ট সেলার / নতুন (optional)"}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '5'}),
            'reviews_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'highlights': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'One highlight per line'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'phone_number', 'address', 'delivery_area',
            'quantity', 'status',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_area': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }


class SiteSettingForm(forms.ModelForm):
    class Meta:
        model = SiteSetting
        fields = [
            'site_name', 'slogan', 'logo',
            'cod_notice', 'helpline', 'whatsapp',
            'hero_badge', 'hero_title', 'hero_subtitle',
            'footer_about',
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cod_notice': forms.TextInput(attrs={'class': 'form-control'}),
            'helpline': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_badge': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'footer_about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
