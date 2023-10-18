from __future__ import annotations

from django.db import models
from django.db.models import F, Sum, Prefetch, ExpressionWrapper

from core.models import BaseQuerySet


class CartQuerySet(BaseQuerySet):
    def active_carts(self) -> CartQuerySet:
        """
        Get only active carts which are not checked out
        """
        return self.filter(checkout_complete=False)

    def with_cart_total(self) -> CartQuerySet:
        return self.annotate(
            total_price=Sum(F("items__product__price") * F("items__quantity"))
        )

    def with_checkout_data(self) -> CartQuerySet:
        from store.models.cart import CartItem

        return (
            self.prefetch_related(
                Prefetch("items", queryset=CartItem.objects.with_total_price()),
                "items__product",
            ).with_cart_total()
            # TODO add promo code discount
            # TODO shipping
        )


class CartItemQuerySet(BaseQuerySet):
    def with_total_price(self) -> CartItemQuerySet:
        return self.annotate(
            total_price=F("quantity") * F("product__price"),
            mada_total_price=F("quantity") * F("product__price"),
        )
