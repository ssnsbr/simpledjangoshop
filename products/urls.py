from django.urls import path
from .views import ProductsViewsets, UserViewSet

from rest_framework.routers import SimpleRouter


# urlpatterns = [
#     path("", ProductsList.as_view(), name="product_list"),
#     path("<uuid:pk>/", ProductDetail.as_view(), name="product_detail"),
# ]
router = SimpleRouter()
router.register("users", UserViewSet, basename="users")
router.register("", ProductsViewsets, basename="products")
urlpatterns = router.urls
