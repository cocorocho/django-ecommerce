from django.urls import path

from core.views import CSRFTestView

app_name = "core"

urlpatterns = [
    path("csrf-test/", CSRFTestView.as_view(), name="csrf-test")
]