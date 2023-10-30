from __future__ import annotations
from datetime import timedelta

from django.utils import timezone
from django.db.models import F, Sum, Prefetch

from core.models import BaseQuerySet
from payments.constants import CHECKOUT_EXPIRE_AGE
from store.models.cart import CartItem


class CheckoutQuerySet(BaseQuerySet):
    def valid(self) -> CheckoutQuerySet:
        """
        Validity of `Checkout` instance is determined by its `date_created`
        field and `CHECKOUT_EXPIRE_AGE`
        """
        return self.annotate(
            expire_date=(F("date_created") + timedelta(seconds=CHECKOUT_EXPIRE_AGE)),
        ).filter(expire_date__gte=timezone.now(), checkout_complete=False)

    def with_checkout_data(self) -> CheckoutQuerySet:
        """
        Annotate price data
        """
        return self.annotate(
            total_price=Sum(
                F("cart__items__product__price") * F("cart__items__quantity")
            ),
        )

    def with_cart_relations(self) -> CheckoutQuerySet:
        """
        Select/Prefetch related cart, cart items, cart user. Annotate cart's `total_price`
        """
        return self.select_related("cart", "cart__user").prefetch_related(
            Prefetch(
                "cart__items",
                queryset=CartItem.objects.select_related("product").with_total_price(),
            )
        )
