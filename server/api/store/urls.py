from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

from store.views import CartViewSet, FeaturedProductsViewSet


router = SimpleRouter()
router.register("cart", CartViewSet, basename="cart")

router.register(
    "product/featured", FeaturedProductsViewSet, basename="featured-product"
)

app_name = "store"

urlpatterns = [
    path("", include(router.urls)),
]
