from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from vendor_products.models import VendorProduct
from vendor_products.permissions import IsOwnerOrReadOnly, IsVendorOwner
from vendor_products.serializers import VendorProductSerializer


class VendorProductViewSets(viewsets.ModelViewSet):  # read only
    permission_classes = [IsOwnerOrReadOnly, IsVendorOwner]
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer

    # def get_object(self):
    #     print("jo")
    #     return super().get_object()
    def update(self, request, *args, **kwargs):
        print("Update:", 10 * "**")
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["vendor_pk"])

        self.check_object_permissions(self.request, obj)
        su = super().update(request, *args, **kwargs)
        print("SU:", su)
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
        pk = self.kwargs.get("pk", None)
        qs = self.queryset.filter(Q(id__exact=pk))
        return qs[0]

    # http_method_names = ["get"] or ReadOnlyModelViewSet



class ProductVendorsViewsets(viewsets.ModelViewSet):  # VendorsOfProductViewSets
    queryset = VendorProduct.objects.all()
    serializer_class = VendorProductSerializer
    # permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        print(10 * "s")
        pk = self.kwargs.get("pk", None)
        res = VendorProduct.objects.filter(Q(product_id__exact=pk))
        print("res", res)
        return self.queryset.filter(Q(product_id__exact=pk))


#     def get_object(self):
#         print(10 * "x")
#         pk = self.kwargs.get("pk", None)
#         return self.queryset.filter(Q(product_id__exact=pk))
#     #     return super().get_object()




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

# class VendorProductViewSet(generics.ListCreateAPIView):
#     queryset = VendorProduct.objects.all()
#     serializer_class = VendorProductSerializer
# permission_classes = [IsAuthenticated]

# def get_queryset(self):
#     user = self.request.user
#     return self.queryset.filter(vendor__user=user)

