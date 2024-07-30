from django.urls import path
from .views import ProductsList, ProductDetail

urlpatterns = [
    path("", ProductsList.as_view(), name="product_list"),
    path("<uuid:pk>/", ProductDetail.as_view(), name="product_detail"),
]
