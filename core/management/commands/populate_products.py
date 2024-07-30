from django.core.management.base import BaseCommand
from faker import Faker
from products.models import Product
from vendors.models import Vendor, VendorProduct
import random

# from users.models import User, Vendor, Category, ProductImage


class Command(BaseCommand):
    help = "Populate the database with fake products and related data"

    def handle(self, *args, **kwargs):
        fake = Faker("fa_IR")  # Persian locale
        # VendorProduct.objects.all().delete()
        # Product.objects.all().delete()
        # Category.objects.all().delete()
        # Vendor.objects.all().delete()
        # Create products and assign to vendors
        product_names = [
            "لباس تکواندو",
            "کمربند مشکی",
            "محافظ دست",
            "کیسه بوکس",
            "محافظ دهان",
            "محافظ ساق پا",
            "ساک ورزشی",
            "بطری آب",
            "محافظ سینه",
            "کتاب آموزش تکواندو",
            "دی وی دی مسابقات",
        ]

        vendor_names = [
            "فروشگاه ورزشی الف",
            "فروشگاه ورزشی ب",
            "فروشگاه ورزشی ج",
        ]
        vendors = []
        for name in vendor_names:
            vendor = Vendor.objects.create(
                # id=Faker("uuid4"),
                store_name=name,
                store_address=fake.text(),
                store_bio=fake.text(),
                contact_number=fake.random_int(min=11111, max=31111),
            )
            vendors.append(vendor)
        products = []
        for name in product_names:
            product = Product.objects.create(
                # id=Faker("uuid4"),
                name=name,
                description=fake.text(),
                price=100,
            )
            products.append(product)
             # Each product can have multiple vendors
            num_vendors = fake.random_int(min=1, max=3)
            selected_vendors = fake.random_elements(elements=vendors, length=num_vendors, unique=True)
            for vendor in selected_vendors:
                VendorProduct.objects.create(
                    product=product,
                    vendor=vendor,
                    price=fake.random_number(digits=5, fix_len=True) / 100,
                    warehouse_quantity=fake.random_int(min=1, max=100),
                    available=True
                )

