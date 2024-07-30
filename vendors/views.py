from django.shortcuts import render

from rest_framework import viewsets

from .models import Vendor, VendorProduct
from .serializers import VendorProductSerializer, VendorSerializer
from rest_framework import viewsets, generics


class VendorViewSet(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return self.queryset.filter(user=self.request.user)


class VendorProductViewSet(generics.ListCreateAPIView):
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     user = self.request.user
    #     return self.queryset.filter(vendor__user=user)
