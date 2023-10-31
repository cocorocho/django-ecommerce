from typing import Iterable
from collections import OrderedDict

from django.db import transaction

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

from core.base.serializers import DynamicFieldsModelSerializer

from products.serializers import StoreProductDetailSerializer
from store.models.cart import Cart, CartItem
from store.models import FeaturedProducts


class CartItemSerializer(serializers.ModelSerializer):
    product = StoreProductDetailSerializer(
        read_only=True,
        fields=("id", "manufacturer", "name", "price", "slug", "thumbnail"),
    )
    # Annotated field
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "total_price")


class CartItemCreateUpdateSerializer(UniqueFieldsMixin, WritableNestedModelSerializer):
    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "cart")
        extra_kwargs = {
            "cart": {"required": False, "write_only": True},
            "product": {"required": False},
        }

    def create(self, validated_data):
        cart = validated_data["cart"]
        product = validated_data["product"]
        quantity = validated_data.get("quantity", 1)

        if cart.product_is_in_cart(product):
            cart_item: CartItem = cart.items.get(product=product)
            cart_item.increment_quantity(quantity)
            return cart_item

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Product is always instance product, can't be updated
        validated_data.update({"product": instance.product})

        return super().update(instance, validated_data)


class CartSerializer(WritableNestedModelSerializer):
    items = CartItemSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = ("user", "items", "session_id")


class CartDetailsReadOnlySerializer(DynamicFieldsModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    # Annotated fields
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    # TODO post discount price
    # TODO shipping
    # TODO taxes

    class Meta:
        model = Cart
        fields = ("user", "items", "session_id", "total_price")
        read_only_fields = fields


class CartWriteUpdateSerializer(WritableNestedModelSerializer):
    items = CartItemCreateUpdateSerializer(many=True, required=False)

    class Meta:
        model = Cart
        fields = ("id", "user", "items", "session_id")

    @transaction.atomic
    def update(self, instance: Cart, validated_data: OrderedDict) -> OrderedDict:
        # Update existing products and quantities instead of creating new `CartItem`
        items = validated_data["items"]
        items_to_update: Iterable[CartItem] = instance.items.filter(
            product__in=[item["product"] for item in items]
        )

        for item_to_update in items_to_update:
            item_data = next(
                filter(lambda i: i["product"] == item_to_update.product, items)
            )
            # Remove from validated data to prevent new `CartItem` creation
            items.remove(item_data)
            # Update existing product
            quantity = item_data["quantity"]
            instance.update_item_quantity(item_to_update, quantity)

        return super().update(instance, validated_data)


class FeaturedProductsReadOnlySerializer(serializers.ModelSerializer):
    products = StoreProductDetailSerializer(many=True)

    class Meta:
        model = FeaturedProducts
        fields = ("slug", "image", "products", "header")
        read_only_fields = fields
