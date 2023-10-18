from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.status import HTTP_201_CREATED

from store.models.cart import Cart
from store.serializers import (
    CartSerializer,
    CartDetailsReadOnlySerializer,
    CartWriteUpdateSerializer,
    CartItemCreateUpdateSerializer,
)
from store.constants import CART_SESSION_COOKIE_KEY


class CartViewSet(
    RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, GenericViewSet
):
    serializer_class = CartSerializer
    lookup_field = "session_id"

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT", "POST", "DELETE"]:
            return CartWriteUpdateSerializer
        elif self.request.method == "GET":
            return CartDetailsReadOnlySerializer

        return super().get_serializer_class()

    def get_queryset(self):
        return Cart.objects.active_carts().with_checkout_data()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response = self.set_cart_session_cookie(response)
        return response

    def set_cart_session_cookie(self, response: Response) -> Response:
        """
        Set cart session cookie
        """
        key = response.data["session_id"]
        response.set_cookie(
            CART_SESSION_COOKIE_KEY,
            key,
        )
        return response

    @action(detail=True, methods=["POST", "PATCH"], url_path="item")
    def add_product(self, request, *args, **kwargs):
        cart = self.get_object()
        request.data.update({"cart": cart.pk})
        serializer = CartItemCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data, status=HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["PATCH"],
        url_path="item/(?P<cart_item_id>[0-9]+)",
        url_name="product-update-delete",
    )
    def update_product(self, request, *args, **kwargs):
        cart = self.get_object()
        cart_item = get_object_or_404(cart.items.all(), id=kwargs.get("cart_item_id"))
        serializer = CartItemCreateUpdateSerializer(
            instance=cart_item, data=request.data
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(serializer.data)

    @update_product.mapping.delete
    def delete_cart_item(self, request, *args, **kwargs):
        cart = self.get_object()
        cart_item_id = kwargs.get("cart_item_id")
        cart_item = get_object_or_404(cart.items.all(), id=cart_item_id)
        cart_item.delete()
        return Response()
