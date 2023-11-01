from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
)
from rest_framework.status import HTTP_201_CREATED

from store.models.cart import Cart
from store.models import Store
from store.serializers import (
    CartSerializer,
    CartDetailsReadOnlySerializer,
    CartWriteUpdateSerializer,
    CartItemCreateUpdateSerializer,
    FeaturedProductsReadOnlySerializer,
)
from products.querysets import ProductQuerySet
from store.services.products import StoreProductService


class GetStoreMetaView(APIView):
    def get_queryset(self):
        return Store.objects.get_store()

    def get(self, request) -> Response:
        queryset = self.get_queryset()
        return Response(queryset)


class CartViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
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


class FeaturedProductsViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = FeaturedProductsReadOnlySerializer
    lookup_field = "slug"

    def get_queryset(self) -> ProductQuerySet:
        return StoreProductService.get_featured()

    def list(self, request):
        queryset = self.get_queryset().values("id", "image", "header", "slug")
        return Response(queryset)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
