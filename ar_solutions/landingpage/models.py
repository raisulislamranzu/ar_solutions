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

class SinglePage(models.Model):
    # Basic
    title = models.CharField(max_length=200, help_text="Page title / Internal name")
    slug = models.SlugField(max_length=200, unique=True, help_text="Unique URL link, e.g. magic-mouse-trap")
    linked_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, help_text="Optional linked product from inventory")
    is_active = models.BooleanField(default=True, help_text="Uncheck to temporarily hide this page")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Top Announcement Bar
    announcement_text = models.CharField(max_length=255, default="🔥 সীমিত সময়ের অফার! স্টক শেষ হওয়ার আগেই অর্ডার করুন! 🔥")

    # Header
    brand_name = models.CharField(max_length=100, blank=True, default="", help_text="Leave blank to use Site Name")
    header_cta_text = models.CharField(max_length=50, default="অর্ডার করুন")

    # Hero Section
    hero_title = models.CharField(max_length=255, default="ইঁদুরের যন্ত্রণায় অতিষ্ঠ? চিরতরে মুক্তি পান ম্যাজিক মাউস ট্র্যাপ দিয়ে!")
    hero_subtitle = models.TextField(blank=True, default="কোনো বিষ বা আঠা ছাড়া, ১০০% নিরাপদ এবং বারবার ব্যবহারযোগ্য।")
    hero_image = models.ImageField(upload_to='landingpages/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, help_text="Optional YouTube embed link")
    auto_scroll_images = models.BooleanField(default=True, help_text="Automatically slide hero gallery images")
    auto_scroll_interval = models.PositiveIntegerField(default=3, help_text="Slide change interval in seconds")

    # Pricing Box
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, default=600)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=450)
    delivery_note = models.CharField(max_length=150, default="সারা বাংলাদেশে ক্যাশ অন ডেলিভারি!")
    hero_cta_text = models.CharField(max_length=50, default="এখনই অর্ডার করুন")

    # Features / Why Choose Us Section
    features_title = models.CharField(max_length=200, default="কেন আমাদের মাউস ট্র্যাপ সেরা?")
    feature_1_icon = models.CharField(max_length=50, default="fas fa-leaf", help_text="FontAwesome icon class")
    feature_1_title = models.CharField(max_length=150, default="১০০% বিষমুক্ত ও নিরাপদ")
    feature_1_desc = models.TextField(default="বাচ্চা বা পোষা প্রাণীর জন্য কোনো ক্ষতিকর বিষ বা রাসায়নিক ব্যবহার করা হয়নি।")

    feature_2_icon = models.CharField(max_length=50, default="fas fa-sync-alt")
    feature_2_title = models.CharField(max_length=150, default="বারবার ব্যবহারযোগ্য")
    feature_2_desc = models.TextField(default="মজবুত প্লাস্টিক দিয়ে তৈরি, ধুয়ে বারবার ব্যবহার করা যায়। একবার কিনলেই চলবে বহুবছর।")

    feature_3_icon = models.CharField(max_length=50, default="fas fa-bolt")
    feature_3_title = models.CharField(max_length=150, default="তাত্ক্ষণিক সমাধান")
    feature_3_desc = models.TextField(default="শক্তিশালী স্প্রিং মেকানিজমের কারণে ইঁদুর ধরা পড়ে চোখের পলকে, পালানোর কোনো সুযোগ নেই।")

    feature_4_icon = models.CharField(max_length=50, default="fas fa-hand-sparkles")
    feature_4_title = models.CharField(max_length=150, default="পরিষ্কার করা সহজ")
    feature_4_desc = models.TextField(default="মৃত ইঁদুর হাত দিয়ে না ধরেই সহজে ফেলে দেওয়া যায়, যা অত্যন্ত স্বাস্থ্যকর।")

    # Delivery charges
    delivery_inside_dhaka = models.IntegerField(default=60)
    delivery_outside_dhaka = models.IntegerField(default=120)

    # Form & Footer
    form_title = models.CharField(max_length=200, default="অর্ডার কনফার্ম করতে নিচের ফর্মটি পূরণ করুন")
    submit_button_text = models.CharField(max_length=100, default="অর্ডার কনফার্ম করুন")
    footer_helpline = models.CharField(max_length=50, blank=True, default="", help_text="Leave blank to use Site Helpline")
    footer_email = models.CharField(max_length=100, blank=True, default="", help_text="Support email")
    footer_copyright = models.CharField(max_length=200, blank=True, default="")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def all_images(self):
        imgs = []
        if self.hero_image:
            imgs.append(self.hero_image.url)
        for img_obj in self.images.all():
            if img_obj.image and img_obj.image.url not in imgs:
                imgs.append(img_obj.image.url)
        if not imgs and self.linked_product and self.linked_product.image:
            imgs.append(self.linked_product.image.url)
        return imgs

    @property
    def embed_video_url(self):
        if not self.video_url:
            return ""
        url = self.video_url.strip()
        if 'youtube.com/embed/' in url:
            return url
        if 'youtube.com/watch?v=' in url:
            try:
                video_id = url.split('watch?v=')[1].split('&')[0]
                return f"https://www.youtube.com/embed/{video_id}"
            except Exception:
                return url
        if 'youtu.be/' in url:
            try:
                video_id = url.split('youtu.be/')[1].split('?')[0]
                return f"https://www.youtube.com/embed/{video_id}"
            except Exception:
                return url
        return url


class SinglePageImage(models.Model):
    single_page = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='landingpages/gallery/')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.single_page.title} - Image #{self.id}"


class SinglePageBundle(models.Model):
    single_page = models.ForeignKey(SinglePage, on_delete=models.CASCADE, related_name='bundles')
    name = models.CharField(max_length=200, help_text="e.g. ১ পিস ম্যাজিক মাউস ট্র্যাপ")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for this bundle")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Original price for strikethrough (optional)")
    quantity = models.PositiveIntegerField(default=1)
    is_default = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.single_page.title} - {self.name} (৳{self.price})"


class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    landing_page = models.ForeignKey(SinglePage, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    package_name = models.CharField(max_length=255, blank=True, null=True)
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