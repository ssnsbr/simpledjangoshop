from django.urls import path
from .views import ProductsMediaViewsets, ProductsViewsets

from rest_framework.routers import SimpleRouter


# urlpatterns = [
#     path("", ProductsList.as_view(), name="product_list"),
#     path("<uuid:pk>/", ProductDetail.as_view(), name="product_detail"),
# ]
router = SimpleRouter()
router.register("", ProductsViewsets, basename="products")
router.register("media", ProductsMediaViewsets, basename="products-media")

urlpatterns = router.urls
