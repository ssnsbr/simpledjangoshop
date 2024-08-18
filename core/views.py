from django.shortcuts import render
from rest_framework import viewsets, generics

# Create your views here.
from django.views.generic import ListView, DetailView
from products.permissions import IsAuthorOrReadOnly
from .serializers import  UserSerializer
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthorOrReadOnly,)
    permission_classes = [IsAdminUser]  # new
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer