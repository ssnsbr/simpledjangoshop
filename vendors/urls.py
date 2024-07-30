from django.urls import path
from .views import VendorProductViewSet, VendorViewSet

urlpatterns = [
    path("<uuid:pk>/", VendorViewSet.as_view(), name="vendor_detail"),
    path("product/<uuid:pk>/", VendorProductViewSet.as_view(), name="vendor_product_detail"),
    path("", VendorProductViewSet.as_view(), name="vendor_product_list"),
]
