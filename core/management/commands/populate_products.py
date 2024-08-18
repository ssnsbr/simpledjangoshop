from os import path
from django.core.management.base import BaseCommand
from definitions import ROOT_DIR
from faker import Faker
from products.models import Category, Product, ProductMedia
from vendors.models import Vendor, VendorProduct
import random
from django.contrib.auth import get_user_model
import glob

# from users.models import User, Vendor, Category, ProductImage


class Command(BaseCommand):
    help = "Populate the database with fake products and related data"

    def handle(self, *args, **kwargs):
        images_list = glob.glob(
            path.join(ROOT_DIR, "static\\img\\saloerphotos\\saloerplaceholders\\*.png")
        )
        images_list = [x[len(ROOT_DIR) :] for x in images_list]
        print(images_list)
        fake = Faker("fa_IR")  # Persian locale
        get_user_model().objects.all().delete()

        # VendorProduct.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Vendor.objects.all().delete()
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

        vendor_users = [
            get_user_model().objects.create_user(
                username="vendor1", email="vendor1@email.com", password="testpass123"
            ),
            get_user_model().objects.create_user(
                username="vendor2", email="vendor2@email.com", password="testpass123"
            ),
            get_user_model().objects.create_user(
                username="vendor3", email="vendor3@email.com", password="testpass123"
            ),
        ]

        self.stdout.write(
            self.style.SUCCESS("Successfully add Vendor Users to the database.")
        )

        for i, name in enumerate(vendor_names):
            vendor = Vendor.objects.create(
                owner=vendor_users[i],
                # id=Faker("uuid4"),
                store_name=name,
                store_address=fake.text(),
                store_bio=fake.text(),
                contact_number=fake.random_int(min=11111, max=31111),
            )
            vendors.append(vendor)
        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with fake vendors")
        )

        products = []
        for name in product_names:
            product = Product.objects.create(
                # id=Faker("uuid4"),
                name=name,
                description=fake.text(),
            )
            products.append(product)
            # Each product can have multiple vendors
            num_vendors = fake.random_int(min=1, max=3)
            selected_vendors = fake.random_elements(
                elements=vendors, length=num_vendors, unique=True
            )
            num_images = fake.random_int(min=1, max=5)
            selected_images = fake.random_elements(
                elements=images_list, length=num_images, unique=True
            )
            for i in selected_images:
                ProductMedia.objects.create(
                    product=product,
                    image=i,
                )

            for vendor in selected_vendors:
                VendorProduct.objects.create(
                    product=product,
                    vendor=vendor,
                    price=fake.random_number(digits=5, fix_len=True) / 100,
                    warehouse_quantity=fake.random_int(min=1, max=100),
                    available=True,
                )
