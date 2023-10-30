from django.utils.translation import gettext_lazy as _
from django.http import HttpRequest, HttpResponse


from rest_framework import serializers
from rest_framework.status import HTTP_404_NOT_FOUND

from store.constants import CART_SESSION_COOKIE_KEY
from store.models.cart import Cart
from payments.exceptions import CheckoutIsNotValid
from payments.models import Checkout
from store.serializers import CartDetailsReadOnlySerializer


def merge_user_cart_with_client_cart(request: HttpRequest, response: HttpResponse):
    cart_session_id = request.COOKIES.get(CART_SESSION_COOKIE_KEY, None)
    user = request.user if request.user.is_authenticated else None

    cart, created = Cart.objects.get_or_create(
        session_id=cart_session_id, defaults={"user": user}
    )

    user_cart: Cart = user.cart

    if cart != user_cart:
        user_cart.merge_carts(cart)

    if created or cart != user_cart:
        cart = user_cart
        response.set_cookie(CART_SESSION_COOKIE_KEY, cart.session_id)


class CartCheckout:
    @staticmethod
    def checkout_create(**kwargs) -> Checkout:
        cart: Cart = kwargs["cart"]

        return Checkout.objects.create(
            price=cart.get_total_price(),
            **kwargs,
        )

    @staticmethod
    def checkout_get(cart: Cart, **kwargs) -> Checkout:
        checkout = cart.checkouts.valid().latest("pk")

        if checkout.is_expired:
            raise CheckoutIsNotValid()

        return checkout

    @staticmethod
    def get_cart_serialized_data(cart: Cart) -> dict:
        """
        Get cart's current serialized data.
        """
        queryset = Cart.objects.with_cart_total_price().with_checkout_data()
        cart = queryset.get(pk=cart.pk)

        return CartDetailsReadOnlySerializer(
            cart,
            fields=("id", "items", "session_id", "total_price"),
        ).data

    @staticmethod
    def checkout_get_or_create(cart: Cart, **kwargs) -> Checkout:
        try:
            checkout = CartCheckout.checkout_get(cart=cart)
        except (Checkout.DoesNotExist, CheckoutIsNotValid):
            checkout = CartCheckout.checkout_create(cart=cart)

        return checkout

    @staticmethod
    def proceed_to_checkout(cart_session_id: str) -> Checkout:
        """
        Get or create `Checkout` instance with given `Cart`
        """

        # Get cart
        try:
            cart = (
                Cart.objects.active_carts()
                .with_cart_total_price()
                .get(session_id=cart_session_id)
            )
        except Cart.DoesNotExist:
            raise serializers.ValidationError(
                _("cart doesn't exist"), HTTP_404_NOT_FOUND
            )

        # Get checkout instance for cart, or create
        checkout = CartCheckout.checkout_get_or_create(cart)

        return checkout
