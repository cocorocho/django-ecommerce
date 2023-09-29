from django.urls import path

from rest_framework.routers import DefaultRouter

from store.views import (
    CategoryViewSet, SubCategoryAPIView
)

app_name = "store"

router = DefaultRouter()
router.register("category", CategoryViewSet)

urlpatterns = [
    *router.urls,
    path("category/<slug:category_slug>/<slug:slug>/", SubCategoryAPIView.as_view()),
]
