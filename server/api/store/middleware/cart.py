from django.http import HttpRequest, HttpResponse

from store.constants import CART_SESSION_COOKIE_KEY
from store.models.cart import Cart


class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)

        self.initialize_cart(request, response)

        return response

    def initialize_cart(self, request: HttpRequest, response: HttpResponse) -> None:
        """
        Check cart through request, If cart session doesn't exist, create new cart
        """
        cart_session_id = request.COOKIES.get(CART_SESSION_COOKIE_KEY, None)

        if not cart_session_id:
            user = None

            if request.user.is_authenticated and not request.user.has_cart:
                user = request.user

            cart = Cart.objects.create(user=user)
            response.set_cookie(CART_SESSION_COOKIE_KEY, cart.session_id)
            return

        if cart_session_id:
            cart, created = Cart.objects.get_or_create(session_id=cart_session_id)

            if not cart.is_valid:
                # Create new cart if not valid
                cart = Cart.objects.create()
                created = True

            if created:
                response.set_cookie(CART_SESSION_COOKIE_KEY, cart.session_id)
