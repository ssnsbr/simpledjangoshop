from rest_framework import serializers
from .models import Payment
from django.contrib.auth import get_user_model

# fields = '__all__'

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
