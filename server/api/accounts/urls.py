from django.urls import path

from rest_framework.routers import DefaultRouter
from djoser.views import UserViewSet

from accounts.views import LoginView, LogoutView, UserAddressViewSet


router = DefaultRouter()
router.register("", UserViewSet, basename="accounts")


address_router = DefaultRouter()
address_router.register("user/address", UserAddressViewSet, basename="user-address")

DJOSER_REQUIRED_ENDPOINTS = (
    "api-root",
    "accounts-list",
    "accounts-reset-password",
    "accounts-reset-password-confirm",
    "accounts-set-password",
)

app_name = "accounts"

urlpatterns = [
    path("signin/", LoginView.as_view(), name="user-signin"),
    path("signout/", LogoutView.as_view(), name="user-signout"),
    *[url for url in router.urls if url.name in DJOSER_REQUIRED_ENDPOINTS],
    *address_router.urls,
]
