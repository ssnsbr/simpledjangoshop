from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import ProductVendorsViewsets, VendorProductViewSets

# Nested routers for vendor-specific routes
vendor_products_router = SimpleRouter()
vendor_products_router.register(
    "products", VendorProductViewSets, basename="vendor-products"
)

vpr = SimpleRouter()
vpr.register("vendors", ProductVendorsViewsets, basename="vp")
vendor_products_router = SimpleRouter()
vendor_products_router.register(
    "products", VendorProductViewSets, basename="vendor-products"
)

urlpatterns = [
    path(
        "<uuid:vendor_pk>/",
        include(vendor_products_router.urls),
        name="vendor_products",
    ),
    path("<str:product_pk>/", include(vpr.urls)),
    path(
        "<uuid:vendor_pk>/",
        include(vendor_products_router.urls),
        name="vendor_products",
    ),
]
