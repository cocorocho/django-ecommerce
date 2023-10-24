from django.shortcuts import get_object_or_404

from rest_framework.response import Response

from core.base.views import GenericAPIView
from payments.models import Checkout
from store.services.cart import CartCheckout
from payments.serializers.checkout import (
    CheckoutReadOnlySerializer,
    FinalizeOrderSerializer,
)


class CheckoutAPIView(GenericAPIView):
    def get_queryset(self):
        return Checkout.objects.all()

    def post(self, request, *args, **kwargs) -> Response:
        cart_session_id = request.data.get("cart_session_id")

        checkout = CartCheckout.proceed_to_checkout(cart_session_id)
        serializer = CheckoutReadOnlySerializer(checkout)

        return Response(serializer.data)

    def get(self, request, token, *args, **kwargs) -> Response:
        checkout = get_object_or_404(Checkout, token=token)

        if checkout.is_expired:
            cart = checkout.cart
            checkout = CartCheckout.checkout_get_or_create(cart)

        serializer = CheckoutReadOnlySerializer(checkout)

        return Response(serializer.data)


class CheckoutFinalizeAPIView(GenericAPIView):
    serializer_class = FinalizeOrderSerializer
    lookup_field = "token"

    def get_queryset(self):
        return Checkout.objects.valid()

    def post(self, request, token, *args, **kwargs) -> Response:
        checkout = self.get_object()
        serializer = self.serializer_class(checkout, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.is_valid())
        return Response()
