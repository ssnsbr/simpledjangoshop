from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from .services import NotificationService

from ..order.models import Transaction
from django.db.models.signals import post_save


User = get_user_model()

@receiver(post_save, sender=User)
def send_registration_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance,
            event="Registration",
            message=f"Welcome {instance.username}! Thank you for registering.",
            notification_type=Notification.EMAIL
        )
        NotificationService.send_notification(notification)

@receiver(post_save, sender=Transaction)
def send_transaction_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            user=instance.user,
            vendor=instance.vendor,
            event="Transaction",
            message=f"Your transaction of {instance.amount} has been processed.",
            notification_type=Notification.EMAIL
        )
        NotificationService.send_notification(notification)

def notify_admins(event, message):
    admins = User.objects.filter(is_staff=True)
    for admin in admins:
        notification = Notification.objects.create(
            admin=True,
            event=event,
            message=message,
            notification_type=Notification.EMAIL
        )
        NotificationService.send_notification(notification)
