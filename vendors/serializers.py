from rest_framework import serializers

from products.serializers import ProductMediaSerialiser
from .models import Vendor, VendorProduct, VendorRating, VendorTransaction

# fields = '__all__'
from drf_spectacular.utils import (
    extend_schema_field,
)


class VendorSerializer(serializers.ModelSerializer):
    # user = Vendor(read_only=True)
    vendor_products = serializers.SerializerMethodField("get_vendor_products")

    def get_vendor_products(self, obj):
        print("vendor_name: obj:", obj.get_vendor_products())
        # data = VendorSerializer(obj.store_name()).data
        data = VendorProductListSerializer(obj.get_vendor_products()).data
        return data

    class Meta:
        model = Vendor
        # fields = ['id', 'user', 'store_name', 'store_bio', 'created_at', 'updated_at']
        fields = "__all__"
        extra_fields = ["vendor_products"]


class VendorProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField("get_vendor_name")
    product_name = serializers.SerializerMethodField("get_product_name")
    product_image = serializers.SerializerMethodField("get_product_image")

    def get_product_image(self, obj):
        data = ProductMediaSerialiser(obj.product.first_image()).data
        return data

    @extend_schema_field(serializers.CharField)
    def get_vendor_name(self, obj):
        return obj.vendor.store_name

    @extend_schema_field(serializers.CharField)
    def get_product_name(self, obj):
        # print("vendor_name: obj:",obj)
        # data = VendorSerializer(obj.store_name()).data
        return obj.product.name

    class Meta:
        model = VendorProduct
        # fields =
        fields = "__all__"
        extra_fields = ["vendor_name", "product_name"]


class VendorProductListSerializer(serializers.ListSerializer):
    child = VendorProductSerializer()


class VendorRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorRating
        fields = "__all__"


class VendorRatingListSerializer(serializers.ListSerializer):
    child = VendorRatingSerializer()


class VendorTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorTransaction
        fields = "__all__"


class VendorTransactionListSerializer(serializers.ListSerializer):
    child = VendorTransactionSerializer()
