from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import VendorProductViewSets, VendorViewsets

# urlpatterns = [
#     path("<uuid:pk>/", VendorViewSet.as_view(), name="vendor_detail"),
#     path("product/<uuid:pk>/", VendorProductViewSet.as_view(), name="vendor_product_detail"),
#     path("", VendorProductViewSet.as_view(), name="vendor_product_list"),
# ]
router = SimpleRouter()
router.register("", VendorViewsets, basename="vendors")

vendorproducts_router = SimpleRouter()
vendorproducts_router.register(
    "", VendorProductViewSets, basename="vendorproducts"
)

# vendor_router = SimpleRouter()
# vendor_router.register("products", VendorProductViewSets, basename="products")

urlpatterns = [
    path("vendors/", include(router.urls)),
    path("vendorproducts/", include(vendorproducts_router.urls)),
    # path("vendorproducts/<str:pk>/", VendorProductViewSets.as_view()),
    # path("a/<int:pk>/", include(vendorproducts_router.urls)),
    # path("<int:pk>/", include(vendor_router.urls)),
]
