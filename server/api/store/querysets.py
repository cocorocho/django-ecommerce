from __future__ import annotations
import typing

from django.db.models import F, Sum, Prefetch

from core.base.models import BaseManager, BaseQuerySet
from store.exceptions import IndeletableStore


class CartQuerySet(BaseQuerySet):
    def active_carts(self) -> CartQuerySet:
        """
        Get only active carts which are not checked out
        """
        return self.filter(checkout_complete=False, merged_to__isnull=True)

    def with_cart_total_price(self) -> CartQuerySet:
        """
        Annotate total price of cart item
        `product.price` * `item.quantity` per item
        `None` is set if `cart` has no items
        """
        return self.annotate(
            total_price=Sum(F("items__product__price") * F("items__quantity"))
        )

    def with_checkout_data(self) -> CartQuerySet:
        from store.models.cart import CartItem

        return (
            self.prefetch_related(
                Prefetch("items", queryset=CartItem.objects.with_total_price()),
                "items__product",
            ).with_cart_total_price()
            # TODO add promo code discount
            # TODO shipping
        )


class CartItemQuerySet(BaseQuerySet):
    def with_total_price(self) -> CartItemQuerySet:
        return self.annotate(
            total_price=F("quantity") * F("product__price"),
            mada_total_price=F("quantity") * F("product__price"),
        )


class StoreQuerySet(BaseQuerySet):
    def delete(self):
        raise IndeletableStore()

    def get_store(self) -> dict[str, typing.Any] | None:
        """
        Store is singleton, first should be the only instance
        """

        DEFER_FIELDS = ("id", "date_created", "date_modified", "_singleton")
        return self.values(
            *[
                field.name
                for field in self.model._meta.local_fields
                if field.name not in DEFER_FIELDS
            ]
        ).first()


class StoreManager(BaseManager):
    def get_queryset(self) -> StoreQuerySet:
        return StoreQuerySet(self.model)

    def delete(self) -> None:
        raise IndeletableStore()
