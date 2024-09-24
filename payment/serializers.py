from rest_framework import serializers
from .models import UserPayment,VendorPayment
from django.contrib.auth import get_user_model

# fields = '__all__'

User = get_user_model()


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"
