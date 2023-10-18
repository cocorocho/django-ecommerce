from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

from store.views import CartViewSet


router = SimpleRouter()
router.register("cart", CartViewSet, basename="cart")

app_name = "store"

urlpatterns = [
    path("", include(router.urls)),
]
