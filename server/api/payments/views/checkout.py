from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from core.base.views import GenericAPIView
from store.services.cart import CartCheckout
from payments.querysets import CheckoutQuerySet
from payments.models import Checkout
from payments.serializers.checkout import (
    CheckoutReadOnlySerializer,
    FinalizeOrderSerializer,
)


class CheckoutAPIView(GenericAPIView):
    serializer_class = CheckoutReadOnlySerializer

    def get_queryset(self) -> CheckoutQuerySet:
        return Checkout.objects.with_cart_relations().with_checkout_data()

    def post(self, request, *args, **kwargs) -> Response:
        cart_session_id = request.data.get("cart_session_id")

        checkout = CartCheckout.proceed_to_checkout(cart_session_id)

        queryset = self.get_queryset()
        checkout = queryset.get(pk=checkout.pk)
        serializer = CheckoutReadOnlySerializer(checkout)

        return Response(serializer.data)

    def get(self, request, token, *args, **kwargs) -> Response:
        queryset = self.get_queryset()
        checkout = get_object_or_404(queryset, token=token)
        response_status = HTTP_200_OK

        if checkout.is_expired or checkout.checkout_complete:
            cart = checkout.cart
            checkout = CartCheckout.checkout_get_or_create(cart)
            response_status = HTTP_201_CREATED

        serializer = CheckoutReadOnlySerializer(checkout, context={"request": request})

        return Response(serializer.data, status=response_status)


class CheckoutFinalizeAPIView(GenericAPIView):
    serializer_class = FinalizeOrderSerializer
    lookup_field = "token"

    def get_queryset(self):
        return Checkout.objects.valid()

    def post(self, request, token, *args, **kwargs) -> Response:
        checkout = self.get_object()
        serializer = self.serializer_class(
            checkout, data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_201_CREATED)
