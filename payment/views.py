from django.shortcuts import render
from django.shortcuts import render

from rest_framework import viewsets

from payment.serializers import PaymentSerializer

from .models import Payment
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework import renderers
from django.db.models import Q


class PaymentViewsets(viewsets.ModelViewSet):  # read only
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
