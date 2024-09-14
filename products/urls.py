from django.urls import include, path
from .views import ProductsMediaViewsets, ProductsViewsets, ProductVendorsViewsets

from rest_framework.routers import SimpleRouter


# urlpatterns = [
#     path("", ProductsList.as_view(), name="product_list"),
#     path("<uuid:pk>/", ProductDetail.as_view(), name="product_detail"),
# ]
router = SimpleRouter()
router.register("", ProductsViewsets, basename="products")

# router.register("<uuid:pk>/vp", ProductVendorsViewsets, basename="vp")
router.register("<uuid:pk>/media", ProductsMediaViewsets, basename="products-media")

# router.register("", ProductsViewsets, basename="products")


vpr = SimpleRouter()
vpr.register("vp", ProductVendorsViewsets, basename="vp")

urlpatterns = [
    path("", include(router.urls)),
    # path("vp/", include(vendor_product_router.urls)),
    # path("vendor-detail/", include(vendor_detail_router.urls)),
    # path("product-detail/", include(product_detail_router.urls)),
    # path("vendorproducts/<str:pk>/", VendorProductViewSets.as_view()),
    # path("a/<int:pk>/", include(vendorproducts_router.urls)),
    path("<str:pk>/", include(vpr.urls)),
]

