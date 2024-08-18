from rest_framework import generics

from . import models
from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    print("UserListView")
    queryset = models.CustomUser.objects.all()
    serializer_class = UserSerializer