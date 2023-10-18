from __future__ import annotations
from collections import OrderedDict

from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from core.models import BaseModel, BaseManager
from store.constants import CART_SESSION_ID_LEN
from store.querysets import CartQuerySet, CartItemQuerySet
from products.models import Product


def generate_cart_session_id() -> str:
    """
    Generate random string `session_id` for `Cart`
    """
    return get_random_string(CART_SESSION_ID_LEN).lower()


class Cart(BaseModel):
    session_id = models.CharField(
        max_length=CART_SESSION_ID_LEN, default=generate_cart_session_id, editable=False
    )
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=_("User"),
        null=True,
        related_name="carts",
    )
    checkout_complete = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_("Cart checked out"),
    )

    objects = BaseManager.from_queryset(CartQuerySet)()

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ("-date_created",)
        # TODO unique together product cart

    def update_item_quantity(self, cart_item: CartItem, quantity: int) -> None:
        """
        Update existing cart product quantity

        :param product Product:     Product instance
        :param int     quantity:    Item quantity
        """
        try:
            cart_item = self.items.get(pk=cart_item.pk)
        except CartItem.DoesNotExist:
            raise ValidationError(_("cart item doesn't exist"))

        if not isinstance(quantity, int):
            raise ValidationError(_("invalid quantity"))

        if quantity < 1:
            # Delete cart item if quantity is less than 1
            cart_item.delete()

        cart_item.quantity = quantity
        cart_item.save()

    def product_is_in_cart(self, product: Product) -> bool:
        """
        Helper method to see if a `Product` already exists in cart
        """
        return self.items.filter(product=product).exists()

    # TODO merge with client cart with server cart if user logs in


class CartItem(BaseModel):
    cart = models.ForeignKey(
        to=Cart, on_delete=models.PROTECT, verbose_name=_("Cart"), related_name="items"
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.PROTECT,
        related_name="cart_items",
        verbose_name=_("Product"),
    )
    quantity = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Item quantity"),
        validators=[
            MinValueValidator(1),
        ],
    )

    objects = BaseManager.from_queryset(CartItemQuerySet)()

    class Meta:
        verbose_name = _("Cart item")
        verbose_name_plural = _("Cart items")
        constraints = [
            models.UniqueConstraint(
                fields=("cart", "product"), name="unique_cart_product"
            )
        ]

    def increment_quantity(self, quantity: int = 1) -> None:
        """
        Increment quantity of cart item
        """
        self.quantity += quantity
        self.save()
