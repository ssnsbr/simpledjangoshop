from django.shortcuts import render
from rest_framework import viewsets, generics

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Product
from .serializers import ProductSerializer


class ProductsList(generics.ListCreateAPIView):  # read only
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):  # read only
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


