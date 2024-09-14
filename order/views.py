from django.shortcuts import render
from rest_framework import viewsets, generics

from cart.models import Cart
from order.models import OrderItem
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CreateOrderFromCartView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.user())

    def user(self):
        return self.request.user

    def cancel_order(self):
        # return orderItems to CartItems
        pass

    def create_order(self):
        cart = Cart.objects.get(user=self.user())

        # Initialize the order total
        total_amount = 0

        # Create a new order
        with transaction.atomic():  # Ensure that the whole order creation is atomic

            order = Order.objects.get_or_create(user=self.user(), total_price=0)

            for cart_item in cart.get_items():
                vendor_product = cart_item.vendor_product

                # Check if enough stock is available
                if vendor_product.warehouse_quantity < cart_item.quantity:
                    return Response(
                        {"error": f"Not enough stock for {vendor_product.name}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Create order items
                order_item = OrderItem.objects.create(
                    order=order,
                    item=vendor_product,
                    quantity=cart_item.quantity,
                    price=vendor_product.price,
                )

                # Update the stock of the product
                vendor_product.warehouse_quantity -= cart_item.quantity
                vendor_product.save()

                # Calculate total amount
                total_amount += vendor_product.price * cart_item.quantity

            # Set the total amount of the order
            order.total_price = total_amount
            order.save()

            # Clear the cart after order is placed
            cart.items.all().delete()
        return order

    def post(self, request):
        order = self.create_order()
        # Return the order details
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class OrderCreateForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ["first_name", "last_name", "email", "address", "city"]
