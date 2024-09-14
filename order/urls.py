from django.urls import include, path
from .views import CreateOrderFromCartView
from rest_framework.routers import SimpleRouter


order_router = SimpleRouter()
order_router.register(
    "order", CreateOrderFromCartView, basename="order_router"
)


urlpatterns = [
    path("", include(order_router.urls)),
    # path("order/", CreateOrderFromCartView.as_view(), name="create_order"),
    # path("order/", order_router, name="create_order"),
]
