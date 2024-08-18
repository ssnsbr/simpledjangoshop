from rest_framework import serializers
from .models import Product
from django.contrib.auth import get_user_model

# fields = '__all__'

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):  # new
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
        )
