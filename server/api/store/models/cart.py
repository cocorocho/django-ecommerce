from __future__ import annotations
from collections.abc import Iterable
from typing import Iterable
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.db import models
from django.db.models import F
from django.contrib.auth import get_user_model

from rest_framework.exceptions import ValidationError

from accounts.models import User
from core.base.models import BaseModel, BaseManager
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
    merged_to = models.ForeignKey(
        to="self",
        on_delete=models.PROTECT,
        editable=False,
        null=True,
        verbose_name=_("Merged carts"),
        related_name="merged_with",
    )

    objects = BaseManager.from_queryset(CartQuerySet)()

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ("-date_created",)
        # TODO unique together product cart

    def save(self, *args, **kwargs) -> None:
        if self.session_id is None:
            self.session_id = generate_cart_session_id()

        return super().save(*args, **kwargs)

    def get_total_price(self) -> Decimal:
        """
        Calculate total price
        """
        return Decimal(
            sum([(item.quantity * item.product.price) for item in self.items.all()])
        )

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

    def merge_carts(self, cart: Cart | Iterable[Cart]) -> "Cart":
        """
        Merge given `cart(s)` `item(s)` to this cart
        """
        # make it iterable so multiple doesn't have to be handled differently
        if not isinstance(cart, Iterable):
            cart = (cart,)

        for _cart in cart:
            items = _cart.items.all()

            common_products = self.items.filter(
                product__pk__in=items.values_list("product__pk")
            ).values_list("product")

            for item in items:
                if common_products.filter(product=item.product).exists():
                    this_cart_item = CartItem.objects.get(
                        product=item.product, cart=self
                    )
                    # Get cart item if exists
                    # Increment quantity if not same
                    if this_cart_item.quantity != item.quantity:
                        this_cart_item.quantity = F("quantity") + item.quantity
                        this_cart_item.save()
                    continue

                # Create new `CartItem` for this cart if doesn't exist
                CartItem.objects.create(
                    product=item.product, cart=self, quantity=item.quantity
                )

            # Set FK `merged_to`
            _cart.merged_to = self
            _cart.save()

        return self

    def appoint_user(self, user: User) -> Cart:
        """
        Appoint user to cart, if user already has an active cart
        client side cart and server side cart will be merged
        """
        if (self.user is not None) and (self.user != user):
            # Possible hijack? Don't appoint user
            return self
        elif self.user is None and user.has_cart:
            # Check if user has an active cart
            # merge this cart instance to user's cart
            user.cart.merge_carts(self)
            return user.cart

        self.user = user
        self.save()
        return self


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
