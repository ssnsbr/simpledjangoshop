from rest_framework import serializers
from .models import Order, OrderItem

from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    vendor = serializers.ReadOnlyField(source='item.vendor.name')  # Fetch the vendor name

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'price', 'quantity', 'get_cost', 'vendor']
        read_only_fields = ['get_cost', 'vendor']
from rest_framework import serializers
from .models import ShippingMethod

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'price']

from rest_framework import serializers
from .models import Order, OrderItem
from accounts.serializers import UserAddressSerializer  # Assuming this serializer exists

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_method = ShippingMethodSerializer(read_only=True)
    address = UserAddressSerializer(read_only=True)
    total_cost = serializers.ReadOnlyField(source='get_total_cost')

    class Meta:
        model = Order
        fields = [
            'id', 
            'user', 
            'total_price', 
            'created_at', 
            'updated_at', 
            'shipping_method', 
            'shipping_cost', 
            'address', 
            'paid', 
            'provider', 
            'items', 
            'total_cost'
        ]
        read_only_fields = ['total_cost', 'created_at', 'updated_at', 'paid']

from rest_framework import serializers
from .models import OrderTracking

class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = [
            'id', 
            'order', 
            'status', 
            'updated_at', 
            'cancellation_requested', 
            'cancellation_approved', 
            'refund_processed', 
            'details'
        ]
        read_only_fields = ['updated_at']
