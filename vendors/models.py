from django.db import models
import uuid
from products.models import Product
from simple import settings
from django.contrib.auth import get_user_model


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="vendor_profile"
    )
    store_name = models.CharField(max_length=255)
    store_address = models.TextField()
    store_bio = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name

    def get_vendor_products(self):
        products = self.vendor_products.all()  # .store_name
        print("store_name:", products)
        return products


# VendorProduct model to handle the many-to-many relationship and additional details
class VendorProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="products"
    )
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="vendor_products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse_quantity = models.PositiveIntegerField()  # stocks
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vendor.store_name} - {self.product.name}"

    def get_vendor_name(self):
        store_name = self.vendor  # .store_name
        # images = [media for media in all_media if media.type == ProductMedia.image]
        print("store_name:", store_name)
        return store_name


class VendorRating(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="vendor_ratings"
    )
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - review of - {self.vendor.store_name}"


class VendorTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(
        Vendor, on_delete=models.CASCADE, related_name="transactions"
    )
    # order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='vendor_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vendor.store_name} - {self.amount}"
