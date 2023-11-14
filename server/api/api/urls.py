"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import SimpleRouter

from core.views.geo import CountryViewSet
from core.views.core import set_csrf_token


geo_router = SimpleRouter()
geo_router.register("countries", CountryViewSet, basename="country")

from cities_light.contrib.restframework3 import router as cities_router

urlpatterns = [
    path("admin/", admin.site.urls),
    # CSRF
    path("set-csrf/", set_csrf_token),
    # Django-Cities-Light
    path("geo/", include(geo_router.urls)),
    # Accounts
    path("account/", include("accounts.urls")),
    # Products
    path("product/", include("products.urls")),
    # Store
    path("store/", include("store.urls")),
    # Payments
    path("checkout/", include("payments.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
        *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    ]
