from django.db import models
from django.contrib.auth import get_user_model
import uuid

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    vendor = models.ForeignKey('vendors.Vendor', on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    admin = models.BooleanField(default=False)
    
    event = models.CharField(max_length=255)  # Registration, Transaction, Sale, etc.
    message = models.TextField()  # Detailed notification message
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'
    
    NOTIFICATION_TYPES = [
        (EMAIL, 'Email'),
        (SMS, 'SMS'),
        (PUSH, 'Push Notification'),
    ]
    
    notification_type = models.CharField(
        max_length=10, choices=NOTIFICATION_TYPES, default=EMAIL
    )

    def __str__(self):
        recipient = self.user if self.user else (self.vendor if self.vendor else "Admin")
        return f"Notification for {recipient} - {self.event}"

