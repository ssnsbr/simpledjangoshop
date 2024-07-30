from django.shortcuts import render
from rest_framework import viewsets, generics

# Create your views here.
from django.views.generic import ListView, DetailView

from products.permissions import IsAuthorOrReadOnly
from .models import Product
from .serializers import ProductSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model

class ProductsViewsets(viewsets.ModelViewSet):  # read only
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]  # new
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
