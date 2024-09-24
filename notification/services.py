from django.core.mail import send_mail
from django.conf import settings
from notification.models import Notification
# from twilio.rest import Client

class NotificationService:
    
    @staticmethod
    def send_email(user, subject, message):
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
    
    @staticmethod
    def send_sms(phone_number, message):
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(
        #     to=phone_number,
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     body=message
        # )
        pass
    
    @staticmethod
    def send_notification(notification):
        if notification.notification_type == Notification.EMAIL:
            NotificationService.send_email(notification.user, notification.event, notification.message)
        elif notification.notification_type == Notification.SMS:
            NotificationService.send_sms(notification.user.profile.phone_number, notification.message)
        # You can add Push notifications here or other channels
