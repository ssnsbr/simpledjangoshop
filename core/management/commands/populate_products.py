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
category_names = ["لباس", "محافظ", "مولتی مدیا"]

product_names_cloth = [
    ["لباس تکواندو", "این لباس لباس تکواندو است!"],
    ["کمربند مشکی", "این کمربند مشکی  است!"],
    ["کیسه بوکس", "این  کیسه بوکس است!"],
    ["ساک ورزشی", "این ساک ورزشی  است!"],
    ["بطری آب", "این بطری  آب است!"],
]
product_names_multimedia = [
    ["کتاب آموزش تکواندو", "این کتاب آموزش تکواندو است!"],
    ["دی وی دی تکواندو", "این دی وی دی تکواندو است!"],
]
product_names_pro = [
    ["محافظ دست", "این محافظ دست است!"],
    ["محافظ دهان", "این محافظ  دهان است!"],
    ["محافظ ساق پا", "این محافظ ساق پا است!"],
    ["محافظ سینه", "این محافظ سینه  است!"],
]
vendor_names = [
    "فروشگاه ورزشی الف",
    "فروشگاه ورزشی ب",
    "فروشگاه ورزشی ج",
]
vendor_bios = [
    "ما فروشگاه ورزشی الف هستیم",
    "ما فروشگاه ورزشی ب هستیم",
    "ما فروشگاه ورزشی ج هستیم",
]


class Command(BaseCommand):
    help = "Populate the database with fake products and related data"

    def populate_categories(self):
        self.categories = []
        for i, cat_name in enumerate(category_names):
            self.categories.append(
                Category.objects.create(
                    name=cat_name, description=cat_name, slug=cat_slugs[i]
                )
            )

    def handle(self, *args, **kwargs):
        images_list = glob.glob(
            path.join(ROOT_DIR, "static\\img\\saloerphotos\\saloerplaceholders\\*.png")
        )
        images_list = [x[len(ROOT_DIR) :] for x in images_list]
        print(images_list)
        fake = Faker("fa_IR")  # Persian locale
        get_user_model().objects.all().delete()

        VendorProduct.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Vendor.objects.all().delete()
        # Create products and assign to vendors
        categories = []
        cat_slugs = ["mo", "le", "mul"]
        for i, cat_name in enumerate(category_names):
            categories.append(
                Category.objects.create(
                    name=cat_name, description=cat_name, slug=cat_slugs[i]
                )
            )

        vendors = []
        customer_users = [
            get_user_model().objects.create_user(
                username="customer_1",
                email="customer_1@email.com",
                password="testpass123",
            ),
            get_user_model().objects.create_user(
                username="customer_2",
                email="customer_2@email.com",
                password="testpass123",
            ),
            get_user_model().objects.create_user(
                username="customer_3",
                email="customer_3@email.com",
                password="testpass123",
            ),
        ]

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
                store_name=name,
                store_address=fake.text(),
                store_bio=vendor_bios[i],
                contact_number=fake.random_int(min=11111, max=31111),
            )
            vendors.append(vendor)
        self.stdout.write(
            self.style.SUCCESS("Successfully populated the database with fake vendors")
        )

        products = []
        for i, cat in enumerate(categories):
            fake_products = [
                product_names_cloth,
                product_names_multimedia,
                product_names_pro,
            ]
            print("8")

            for name, descp in fake_products[i]:
                product = Product.objects.create(
                    name=name,
                    category=cat,
                    description=descp,
                )
                print("9")

                products.append(product)
                # Each product can have multiple vendors
                num_vendors = fake.random_int(min=1, max=3)
                selected_vendors = fake.random_elements(
                    elements=vendors, length=num_vendors, unique=True
                )
                print("10")
                num_images = fake.random_int(min=1, max=5)
                selected_images = fake.random_elements(
                    elements=images_list, length=num_images, unique=True
                )
                print("11")
                for i in selected_images:
                    ProductMedia.objects.create(
                        product=product,
                        image=i,
                    )
                print("12")

                for vendor in selected_vendors:
                    VendorProduct.objects.create(
                        product=product,
                        vendor=vendor,
                        price=fake.random_number(digits=5, fix_len=True) / 100,
                        warehouse_quantity=fake.random_int(min=1, max=100),
                        available=True,
                    )
            self.stdout.write(
                self.style.SUCCESS(f"Successfully added  ${cat} to the database.")
            )
