from django.shortcuts import render

from rest_framework import viewsets

from .models import Vendor, VendorProduct
from .serializers import (
    VendorProductListSerializer,
    VendorProductSerializer,
    VendorSerializer,
)
from rest_framework import viewsets, generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework import renderers
from django.db.models import Q


class VendorViewsets(viewsets.ModelViewSet):  # read only
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorProductViewSets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductListSerializer
    # def get_object(self):
    #     print("jo")
    #     return super().get_object()

    def get_queryset(self):
        print(10 * "s")
        pk = self.kwargs.get("pk", None)
        res = VendorProduct.objects.filter(Q(product_id__exact=pk))
        print("res", res)
        return self.queryset.filter(Q(product_id__exact=pk))

    def get_object(self):
        print(10 * "x")
        pk = self.kwargs.get("pk", None)
        return self.queryset.filter(Q(product_id__exact=pk))

    # http_method_names = ["get"] or ReadOnlyModelViewSet


# class VendorViewSet(generics.ListCreateAPIView):
#     queryset = Vendor.objects.all()
#     serializer_class = VendorSerializer
# permission_classes = [IsAuthenticated]

# def get_queryset(self):
#     return self.queryset.filter(user=self.request.user)


# class VendorProductViewSet(generics.ListCreateAPIView):
#     queryset = VendorProduct.objects.all()
#     serializer_class = VendorProductSerializer
# permission_classes = [IsAuthenticated]

# def get_queryset(self):
#     user = self.request.user
#     return self.queryset.filter(vendor__user=user)
