from django.shortcuts import render

from rest_framework import viewsets

from .models import Vendor, VendorProduct, VendorTransaction
from .serializers import *
from rest_framework import viewsets, generics
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework import renderers
from django.db.models import Q


class VendorViewsets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


# class VendorsOfProductViewSets(viewsets.ModelViewSet):  # read only
#     # permission_classes = (IsOwnerOrReadOnly,)
#     queryset = VendorProduct.objects.all()
#     serializer_class = VendorsOfProductListSerializer
#     # def get_object(self):
#     #     print("jo")
#     #     return super().get_object()

#     def get_queryset(self):
#         print(10 * "s")
#         pk = self.kwargs.get("pk", None)
#         res = VendorProduct.objects.filter(Q(product_id__exact=pk))
#         print("res", res)
#         return self.queryset.filter(Q(product_id__exact=pk))

#     def get_object(self):
#         print(10 * "x")
#         pk = self.kwargs.get("pk", None)
#         return self.queryset.filter(Q(product_id__exact=pk))


class VendorProductViewSets(viewsets.ModelViewSet):  # read only
    permission_classes = (IsOwnerOrReadOnly,)
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    # def get_object(self):
    #     print("jo")
    #     return super().get_object()
    def update(self, request, *args, **kwargs):
        print("Update:",100*"**")
        su = super().update(request, *args, **kwargs)
        print("SU:",su)
        return su

    def get_queryset(self):
        print("get_queryset")
        product_id = self.request.GET.get("p", None)
        res = None
        if product_id:
            res = VendorProduct.objects.filter(Q(product_id__exact=product_id))

        vendor_id = self.request.GET.get("v", None)

        if vendor_id:
            res = VendorProduct.objects.filter(Q(vendor_id__exact=vendor_id))
        print("product_id", vendor_id, product_id)

        if res:
            print("res", res)
            return res
        else:
            return VendorProduct.objects.all()

    def get_object(self):
        
        
        print(10 * "x")
        print(self.kwargs)
        pk = self.kwargs.get("pk", None)
        print(pk)
        qs=self.queryset.filter(Q(id__exact=pk))
        print(qs)
        return qs[0]

    # http_method_names = ["get"] or ReadOnlyModelViewSet


# class ProductsOfVendorViewSets(viewsets.ModelViewSet):  # read only
#     # permission_classes = (IsOwnerOrReadOnly,)
#     queryset = VendorProduct.objects.all()
#     serializer_class = ProductsOfVendorListSerializer
#     # def get_object(self):
#     #     print("jo")
#     #     return super().get_object()

#     def get_queryset(self):
#         # request.GET.get('q', 'default').

#         print(10 * "s")
#         pk = self.kwargs.get("pk", None)
#         res = VendorProduct.objects.filter(Q(vendor_id__exact=pk))
#         print("res", res)
#         return self.queryset.filter(Q(vendor_id__exact=pk))

#     def get_object(self):
#         print(10 * "x")
#         pk = self.kwargs.get("pk", None)
#         return self.queryset.filter(Q(vendor_id__exact=pk))

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


class VendorRatingViewsets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = VendorRating.objects.all()
    serializer_class = VendorRatingSerializer


class VendorTransactionViewsets(viewsets.ModelViewSet):  # read only
    # permission_classes = (IsOwnerOrReadOnly,)
    queryset = VendorTransaction.objects.all()
    serializer_class = VendorTransactionSerializer
