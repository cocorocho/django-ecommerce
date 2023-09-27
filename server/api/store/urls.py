from django.urls import path

from rest_framework.routers import DefaultRouter

from store.views import CategoryViewSet, CategoryProductsViewSet


app_name = "store"

router = DefaultRouter()
router.register("category", CategoryViewSet)

urlpatterns = [
    *router.urls,
    path("categories/<slug:category_slug>/", CategoryProductsViewSet.as_view(), name="category_products")
]
