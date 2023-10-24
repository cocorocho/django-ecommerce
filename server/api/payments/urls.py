from django.urls import path

from payments.views.checkout import CheckoutAPIView, CheckoutFinalizeAPIView


app_name = "payments"

urlpatterns = [
    path("", CheckoutAPIView.as_view(), name="checkout-create"),
    path("<uuid:token>/", CheckoutAPIView.as_view(), name="checkout-retrieve"),
    path(
        "<uuid:token>/complete/",
        CheckoutFinalizeAPIView.as_view(),
        name="checkout-finalize",
    ),
]
