from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, help_text="Unique URL-friendly name")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this category from the public site")

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="AR SOLUTIONS BD")
    slogan = models.CharField(max_length=200, default="Smart Solutions for Everyday Life")
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)

    # --- Editable website content (managed from the custom admin) ---
    cod_notice = models.CharField(max_length=200, default="সারাদেশে ক্যাশ অন ডেলিভারি (COD) সুবিধা!")
    helpline = models.CharField(max_length=20, default="01700-000000")
    whatsapp = models.CharField(max_length=20, default="8801700000000", help_text="WhatsApp number including country code, e.g. 8801700000000")

    hero_badge = models.CharField(max_length=100, blank=True, default="স্মার্ট সল্যুশন")
    hero_title = models.CharField(max_length=200, blank=True, default="সবচেয়ে ভালো পণ্য, ক্যাশ অন ডেলিভারিতে")
    hero_subtitle = models.TextField(blank=True, default="১০০% অরিজিনাল ও প্রবলেম-সলভিং প্রোডাক্ট। সারাদেশে হোম ডেলিভারি সুবিধা।")

    footer_about = models.TextField(blank=True, default="AR SOLUTIONS BD — আপনার বিশ্বস্ত স্মার্ট সল্যুশন পার্টনার।")

    def __str__(self):
        return self.site_name

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique URL link")
    description = models.TextField()
    regular_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="YouTube video embed link")
    delivery_inside_dhaka = models.IntegerField(default=60)
    delivery_outside_dhaka = models.IntegerField(default=120)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this product from the public site")

    # --- Extra display fields for the store front ---
    badge = models.CharField(max_length=50, blank=True, help_text="Optional corner badge, e.g. 'বেস্ট সেলার' or 'নতুন'")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    reviews_count = models.IntegerField(default=0)
    highlights = models.TextField(blank=True, help_text="Enter one highlight per line. Shown in the product Quick View.")

    def __str__(self):
        return self.title

    @property
    def discount_percent(self):
        try:
            if self.regular_price and self.regular_price > 0:
                return int(round((self.regular_price - self.discount_price) / self.regular_price * 100))
        except Exception:
            pass
        return 0

    @property
    def highlight_list(self):
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    delivery_area = models.CharField(max_length=50, choices=[('Inside Dhaka', 'Inside Dhaka'), ('Outside Dhaka', 'Outside Dhaka')])
    quantity = models.IntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            max_id = Order.objects.aggregate(models.Max('id'))['id__max']
            if not max_id or max_id < 1000:
                self.id = 1001
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"