from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import VendorViewsets, VendorProductViewSets, VendorRatingViewsets, VendorTransactionViewsets

# Main vendor router
router = SimpleRouter()
router.register("", VendorViewsets, basename="vendors")

# Nested routers for vendor-specific routes
vendor_products_router = SimpleRouter()
vendor_products_router.register("products", VendorProductViewSets, basename="vendor-products")

vendor_rating_router = SimpleRouter()
vendor_rating_router.register("ratings", VendorRatingViewsets, basename="vendor-ratings")

vendor_transaction_router = SimpleRouter()
vendor_transaction_router.register("transactions", VendorTransactionViewsets, basename="vendor-transactions")

urlpatterns = [
    path("", include(router.urls)),  # Base route for vendors
    path("<uuid:vendor_pk>/", include(vendor_products_router.urls), name="vendor_products"),
    path("<uuid:vendor_pk>/", include(vendor_rating_router.urls), name="vendor_ratings"),
    path("<uuid:vendor_pk>/", include(vendor_transaction_router.urls), name="vendor_transactions"),
    
]
