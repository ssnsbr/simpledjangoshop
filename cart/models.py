import uuid
from django.db import models

from accounts.models import CustomUser
from products.models import Product
from vendors.models import VendorProduct
from django.contrib.auth import get_user_model


# Cart model to handle user's shopping cart
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"


# CartItem model to handle individual items within a cart
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    vendor_product = models.ForeignKey(
        VendorProduct, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"CartItem: {self.vendor_product.product.name} (x{self.quantity}) in cart of {self.cart.user.username}"
