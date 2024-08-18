from rest_framework import serializers
from .models import Vendor, VendorProduct

# fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    # user = Vendor(read_only=True)

    class Meta:
        model = Vendor
        # fields = ['id', 'user', 'store_name', 'store_bio', 'created_at', 'updated_at']
        fields = "__all__"


class VendorProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProduct
        # fields =
        fields = "__all__"


class VendorProductListSerializer(serializers.ListSerializer):
    child=VendorProductSerializer()

