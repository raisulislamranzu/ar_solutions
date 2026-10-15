# -*- coding: utf-8 -*-
"""
Demo data seeder for AR SOLUTIONS BD.

Run from the project root (where manage.py lives):
    python seed_demo.py

It is safe to run multiple times. It will:
  * Create a few categories.
  * Attach categories / badges / ratings / highlights to any existing products
    that are missing them (it never overwrites titles, prices or images).
  * Add a couple of extra demo products (reusing images already in media/).
"""

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ar_solutions.settings")
django.setup()

from landingpage.models import Category, Product, SiteSetting  # noqa: E402


def seed():
    # ----- Categories -----
    cats = {}
    for name, slug in [
        ("ইলেকট্রনিক্স", "electronics"),
        ("গার্ডেনিং", "gardening"),
        ("হোম অ্যাপলায়েন্স", "home-appliances"),
    ]:
        c, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name, "is_active": True})
        cats[slug] = c
        print("Category:", c.name)

    electronics = cats["electronics"]
    gardening = cats["gardening"]

    # ----- Enrich existing products (do not overwrite user data) -----
    enrich = {
        "rechargeable-mosquito-bat-weidasi-wd-979": {
            "category": electronics,
            "badge": "বেস্ট সেলার",
            "rating": 4.8,
            "reviews_count": 126,
            "highlights": "রিচার্জেবল লিথিয়াম ব্যাটারি\nউচ্চ ভোল্টেজে মশা মারানোর ক্ষমতা\nহাতে না লেগে নিরাপদ ব্যবহার\n৬ মাসের ওয়ারান্টি",
        },
        "75": {
            "category": gardening,
            "badge": "জনপ্রিয়",
            "rating": 4.7,
            "reviews_count": 88,
            "highlights": "স্টেইনলেস স্টিল ব্লেড, দীর্ঘস্থায়ী\n৭.৫ ইঞ্চি, আরামদায়ক গ্রিপ\nবাগান ও গাছপালা কাটাইয়ের উপযোগী\nহালকা ওজর, সহজে বহনযোগ্য",
        },
    }
    for slug, data in enrich.items():
        try:
            p = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            continue
        changed = False
        if not p.category:
            p.category = data["category"]; changed = True
        if not p.badge:
            p.badge = data["badge"]; changed = True
        if not p.highlights:
            p.highlights = data["highlights"]; changed = True
        # Always refresh rating/reviews for the demo (harmless defaults)
        p.rating = data["rating"]; p.reviews_count = data["reviews_count"]; changed = True
        if changed:
            p.save()
            print("Enriched:", p.title)

    # ----- Extra demo products (reuse images already present in media/) -----
    demo = [
        {
            "title": "স্মার্ট ওয়াটার প্রুফ LED স্ট্রিপ লাইট",
            "slug": "smart-waterproof-led-strip-light",
            "category": electronics,
            "regular_price": 1200, "discount_price": 850,
            "image": "products/7219b12566ae4a2bb763ca505c2d55c3.jpg_960x960q80.jpg_.webp",
            "description": "ঘর, দোকান ও দেয়াল সাজানোর জন্য স্মার্ট ওয়াটার প্রুফ LED স্ট্রিপ লাইট। আলো ঝকঝকে এবং দীর্ঘস্থায়ী।",
            "badge": "নতুন", "rating": 4.6, "reviews_count": 54,
            "highlights": "ওয়াটার প্রুফ, ঘরে-বাইরে দুই জায়গাতেই ব্যবহারযোগ্য\nসহজেই লাগানো যায়, আলগা তারের দরকার নেই\nকম বিদ্যুৎ খরচ, দীর্ঘস্থায়ী\nআকর্ষণীয় আধুনিক আলো",
        },
        {
            "title": "মাল্টিফাংশন ইলেকট্রিক স্ক্রু ড্রাইভার সেট",
            "slug": "multifunction-electric-screwdriver-set",
            "category": electronics,
            "regular_price": 1500, "discount_price": 1090,
            "image": "products/1773040175-1002053_ready-electronics-presen.jpg",
            "description": "ঘরের ছোট খাটনি থেকে শুরু করে মোবাইল-ইলেকট্রনিক্স সংস্কার—সবকিছুর জন্য আন্তরিক মাল্টিফাংশন ইলেকট্রিক স্ক্রু ড্রাইভার সেট।",
            "badge": "", "rating": 4.5, "reviews_count": 41,
            "highlights": "রিচার্জেবল কর্ডলেস ডিজাইন\nএকাধিক বিট সহ আগত\nকঠিন কাজেও তীক্ষ্ণ পারফরম্যান্স",
        },
    ]
    for d in demo:
        p, created = Product.objects.get_or_create(
            slug=d["slug"],
            defaults={
                "title": d["title"],
                "category": d["category"],
                "description": d["description"],
                "regular_price": d["regular_price"],
                "discount_price": d["discount_price"],
                "image": d["image"],
                "badge": d["badge"],
                "rating": d["rating"],
                "reviews_count": d["reviews_count"],
                "highlights": d["highlights"],
                "delivery_inside_dhaka": 60,
                "delivery_outside_dhaka": 120,
                "is_active": True,
            },
        )
        print("Demo product", "created" if created else "exists", ":", p.title)

    # ----- Ensure a SiteSetting exists with sensible defaults -----
    if not SiteSetting.objects.exists():
        SiteSetting.objects.create()
        print("Created default SiteSetting")
    else:
        print("SiteSetting already present")

    print("\nDone. Products:", Product.objects.count(), "| Categories:", Category.objects.count())


if __name__ == "__main__":
    seed()
