from django import forms
from django.forms import inlineformset_factory
from landingpage.models import Product, Category, Order, SiteSetting, SinglePage, SinglePageBundle


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


class SinglePageForm(forms.ModelForm):
    class Meta:
        model = SinglePage
        fields = [
            'title', 'slug', 'linked_product', 'is_active',
            'announcement_text', 'brand_name', 'header_cta_text',
            'hero_title', 'hero_subtitle', 'hero_image', 'video_url',
            'regular_price', 'discount_price', 'delivery_note', 'hero_cta_text',
            'features_title',
            'feature_1_icon', 'feature_1_title', 'feature_1_desc',
            'feature_2_icon', 'feature_2_title', 'feature_2_desc',
            'feature_3_icon', 'feature_3_title', 'feature_3_desc',
            'feature_4_icon', 'feature_4_title', 'feature_4_desc',
            'delivery_inside_dhaka', 'delivery_outside_dhaka',
            'form_title', 'submit_button_text',
            'footer_helpline', 'footer_email', 'footer_copyright',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Magic Mouse Trap'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. magic-mouse-trap'}),
            'linked_product': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'announcement_text': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave empty for default Site Name'}),
            'header_cta_text': forms.TextInput(attrs={'class': 'form-control'}),

            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'hero_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/embed/...'}),

            'regular_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'discount_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_note': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_cta_text': forms.TextInput(attrs={'class': 'form-control'}),

            'features_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_1_icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-leaf'}),
            'feature_1_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_1_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            'feature_2_icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-sync-alt'}),
            'feature_2_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_2_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            'feature_3_icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-bolt'}),
            'feature_3_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_3_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            'feature_4_icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fas fa-hand-sparkles'}),
            'feature_4_title': forms.TextInput(attrs={'class': 'form-control'}),
            'feature_4_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),

            'delivery_inside_dhaka': forms.NumberInput(attrs={'class': 'form-control'}),
            'delivery_outside_dhaka': forms.NumberInput(attrs={'class': 'form-control'}),

            'form_title': forms.TextInput(attrs={'class': 'form-control'}),
            'submit_button_text': forms.TextInput(attrs={'class': 'form-control'}),

            'footer_helpline': forms.TextInput(attrs={'class': 'form-control'}),
            'footer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'footer_copyright': forms.TextInput(attrs={'class': 'form-control'}),
        }


SinglePageBundleFormSet = inlineformset_factory(
    SinglePage,
    SinglePageBundle,
    fields=['name', 'price', 'original_price', 'quantity', 'is_default', 'order'],
    extra=1,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ১ পিস ম্যাজিক মাউস ট্র্যাপ'}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '450'}),
        'original_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '600 (optional)'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'order': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)
