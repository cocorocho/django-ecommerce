from django.http import HttpRequest, HttpResponse

from store.constants import CART_SESSION_COOKIE_KEY
from store.models.cart import Cart


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
