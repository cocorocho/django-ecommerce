from django.urls import path

from rest_framework.routers import DefaultRouter

from store.views import (
    CategoryViewSet, SubCategoryProductsListView
)

app_name = "store"

router = DefaultRouter()
router.register("category", CategoryViewSet)

urlpatterns = [
    *router.urls,
    path("category/<slug:category_slug>/<slug:sub_category_slug>/", SubCategoryProductsListView.as_view()),
]
