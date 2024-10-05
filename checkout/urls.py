from django.urls import include, path
from .views import PaymentViewsets

from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", PaymentViewsets, basename="checkout")

urlpatterns = [
    path("", include(router.urls)),
]
