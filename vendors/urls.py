from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import *

router = SimpleRouter()
router.register("", VendorViewsets, basename="vendors")


vendor_products_router = SimpleRouter()
vendor_products_router.register("products", VendorProductViewSets, basename="vendors")

vendor_rating_router = SimpleRouter()
vendor_rating_router.register("ratings", VendorRatingViewsets, basename="ratings")

vendor_transaction_router = SimpleRouter()
vendor_transaction_router.register(
    "transactions", VendorTransactionViewsets, basename="transactions"
)

urlpatterns = [
    path("", include(router.urls)),
    # path("vp/", include(vendor_product_router.urls)),
    # path("vendor-detail/", include(vendor_detail_router.urls)),
    # path("product-detail/", include(product_detail_router.urls)),
    # path("vendorproducts/<str:pk>/", VendorProductViewSets.as_view()),
    # path("a/<int:pk>/", include(vendorproducts_router.urls)),
    #     path("<uuid:pk>/", VendorViewSet.as_view(), name="vendor_detail"),
    #     path("product/<uuid:pk>/", VendorProductViewSet.as_view(), name="vendor_product_detail"),
    #     path("", VendorProductViewSet.as_view(), name="vendor_product_list"),
    path("<uuid:pk>/", include(vendor_products_router.urls), name="vendor_products"),
    path("<uuid:pk>/", include(vendor_rating_router.urls),name="vendor_rating"),
    path("<uuid:pk>/", include(vendor_transaction_router.urls),name="vendor_transaction"),
]
