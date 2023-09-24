from django.urls import path, include

from rest_framework.routers import DefaultRouter
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet


router = DefaultRouter()
router.register("", UserViewSet, basename="accounts")

DJOSER_REQUIRED_ENDPOINTS = (
    "api-root",
    "accounts-list",
    "accounts-reset-password",
    "accounts-reset-password-confirm",
    "accounts-set-password",
)

app_name = "accounts"

urlpatterns = [
    path("login/", TokenCreateView.as_view(), name="login"),
    path("logout/", TokenDestroyView.as_view(), name="logout"),
    *[url for url in router.urls if url.name in DJOSER_REQUIRED_ENDPOINTS]
]
