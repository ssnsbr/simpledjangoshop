from django.db import models
import uuid
# from users.models import CustomUser
from products.models import Product


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = models.OneToOneField(
    #     CustomUser, on_delete=models.CASCADE, related_name="vendor"
    # )
    store_name = models.CharField(max_length=255)
    store_address = models.TextField()
    store_bio = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.store_name

# VendorProduct model to handle the many-to-many relationship and additional details
class VendorProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    warehouse_quantity = models.PositiveIntegerField() # stocks
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.vendor.store_name} - {self.product.name}"


# class VendorRating(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     vendor = models.ForeignKey(
#         VendorProfile, on_delete=models.CASCADE, related_name="ratings"
#     )
#     user = models.ForeignKey(
#         CustomUser, on_delete=models.CASCADE, related_name="vendor_ratings"
#     )
#     rating = models.PositiveSmallIntegerField()
#     review = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.vendor.company_name}"


# class VendorTransaction(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     vendor = models.ForeignKey(
#         VendorProfile, on_delete=models.CASCADE, related_name="transactions"
#     )
#     # order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='vendor_transactions')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.vendor.company_name} - {self.amount}"
