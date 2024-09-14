from rest_framework import serializers
from .models import Product, ProductMedia
from django.contrib.auth import get_user_model

# fields = '__all__'
from drf_spectacular.utils import (
    extend_schema_field,
)

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField("get_first_image")


    def get_first_image(self, ins):
        data = ProductMediaSerialiser(ins.first_image()).data
        return {"image_url": data["image_url"], "image": data["image"]}

    class Meta:
        model = Product
        # fields = ['id', 'username', 'email']
        fields = "__all__"
        extra_fields = ["first_image"]


class ProductMediaSerialiser(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = ProductMedia
        fields = "__all__"
        extra_fields = ["image_url"]

    @extend_schema_field(serializers.ImageField)
    def get_image_url(self, obj):
        return obj.image


class ProductMediaListSerializer(serializers.ListSerializer):
    child = ProductMediaSerialiser()
