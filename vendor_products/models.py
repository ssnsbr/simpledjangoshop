import uuid
from django.db import models

from products.models import Product
from vendors.models import Vendor, VendorDiscount


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
    discount = models.ForeignKey(
        VendorDiscount, null=True, on_delete=models.CASCADE, related_name="discount"
    )

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.warehouse_quantity == 0:
            self.available = False
        else:
            self.available = True
        super(VendorProduct, self).save(*args, **kwargs)

    class Meta:
        # unique_together = ('vendor', 'product',)
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "product"], name="vendor product constraint"
            )
        ]
        indexes = [
            models.Index(fields=["vendor", "product"]),
            models.Index(fields=["available"]),
        ]

    def __str__(self):
        return f"{self.vendor.store_name} - {self.product.name}"

    def get_vendor_name(self):
        store_name = self.vendor.store_name  # .store_name
        # images = [media for media in all_media if media.type == ProductMedia.image]
        print("store_name:", store_name)
        return store_name
