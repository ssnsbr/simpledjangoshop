import uuid
from django.db import models
from django.contrib.auth import get_user_model

from order.models import Order
from vendors.models import Vendor, VendorProduct

CustomUser = get_user_model()


# Create your models here.
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="users_payment"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="orders_payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    success = models.BooleanField(default=False)
    status = models.CharField(max_length=255)