"""
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cart/", include("cart.urls")),
    path("api/", include("products.urls")),
    path("api/vendors/", include("vendors.urls")),
    path("api/vendor-product/", include("vendor_products.urls")),
    path("api/orders/", include("order.urls")),
    path("api/payments/", include("payment.urls")),
    path("api/", include("search.urls")),
    # path("accounts/", include("django.contrib.auth.urls")), 
    path("api/dj-rest-auth/", include("dj_rest_auth.urls")),
    path(
        "api/dj-rest-auth/registration/",
        include("dj_rest_auth.registration.urls"),
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
