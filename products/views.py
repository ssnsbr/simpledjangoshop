from django.shortcuts import render
from rest_framework import viewsets, generics
from products.permissions import IsAuthorOrReadOnly
from .models import Product, ProductMedia
from .serializers import ProductSerializer, ProductMediaListSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from django.db.models import Q


class ProductsViewsets(viewsets.ModelViewSet):  # read only
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductsMediaViewsets(viewsets.ModelViewSet):  # read only
    queryset = ProductMedia.objects.all()
    serializer_class = ProductMediaListSerializer

    def get_queryset(self):
        print(10 * "s")
        pk = self.kwargs.get("pk", None)
        res = ProductMedia.objects.filter(Q(product_id__exact=pk))
        print("res", res)
        res2 = self.queryset.filter(Q(product_id__exact=pk))
        print("res2 0", res2[0].image)
        return res

    def get_object(self):
        print(10 * "x")
        pk = self.kwargs.get("pk", None)
        res2 = self.queryset.filter(Q(product_id__exact=pk))
        print("res2 0 ", res2[0])
        return res2
