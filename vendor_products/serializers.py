from typing import Any, Dict
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from products.serializers import ProductMediaSerialiser
from vendor_products.models import VendorProduct


class VendorProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField("get_vendor_name")
    product_name = serializers.SerializerMethodField("get_product_name")
    product_image = serializers.SerializerMethodField("get_product_image")

    # @extend_schema_field(serializers.JSONField)
    def get_product_image(self, obj) -> Dict[str, Any]:
        data = ProductMediaSerialiser(obj.product.first_image()).data
        return data

    @extend_schema_field(serializers.CharField)
    def get_vendor_name(self, obj) -> Dict[str, Any]:
        print(":", obj)
        try:
            return obj.vendor.store_name
        except:
            return True

    @extend_schema_field(serializers.CharField)
    def get_product_name(self, obj) -> Dict[str, Any]:
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
