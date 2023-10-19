import random
from itertools import cycle

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.status import HTTP_200_OK
from rest_framework.reverse import reverse
from model_bakery import baker

from store.constants import CART_SESSION_COOKIE_KEY
from store.models.cart import Cart


class TestUsersEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_djoser_list_users_endpoint(self) -> None:
        URL = reverse("accounts:accounts-list")
        user = baker.make(get_user_model())

        self.client.force_login(user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 404)

    def test_cart_merging_on_user_signin(self) -> None:
        # Create user
        user = get_user_model().objects.create_user(
            email="test@example.com", password="123456"
        )

        # Create client_side cart via endpoint
        url = "/"
        response = self.client.get(url)
        client_side_cart_session_id = response.cookies.get(
            CART_SESSION_COOKIE_KEY
        ).value
        client_cart = Cart.objects.get(session_id=client_side_cart_session_id)
        # Add some products to client side cart
        num_client_cart_items = 5
        quantities = [random.randint(1, 10) for _ in range(num_client_cart_items)]
        client_cart_items = baker.make_recipe(
            "store.tests.cart_item",
            cart=client_cart,
            quantity=cycle(quantities),
            _quantity=num_client_cart_items,
        )

        # Create user cart
        user_cart = baker.make_recipe("store.tests.cart", user=user)
        # Pick one client cart item to increment quantity
        client_cart_item = random.choice(client_cart_items)

        num_user_cart_items = 3
        common_item_cart_quantity = 5
        user_cart_common_item = baker.make_recipe(
            "store.tests.cart_item",
            cart=user_cart,
            product=client_cart_item.product,
            quantity=common_item_cart_quantity,
        )
        new_items = baker.make_recipe(
            "store.tests.cart_item", cart=user_cart, _quantity=num_user_cart_items
        )

        # login user
        url = reverse("accounts:user-signin")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "123456"}
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

        # At this point response should set cookie with user's cart session_id
        self.assertEqual(
            response.cookies.get(CART_SESSION_COOKIE_KEY).value, user_cart.session_id
        )

        # Validate

        # Validate client_side cart `merged_to` is set to `user_cart``
        client_cart.refresh_from_db()
        self.assertEqual(client_cart.merged_to, user_cart)

        # Validate merged cart
        # Num items should be 8:
        #   5 from client cart
        #   3 from existing user cart
        #   one item was in both carts, quantity will be summed

        self.assertEqual(user_cart.items.count(), 8)
        # Validate quantity of common product
        expected_quantity = (
            client_cart_item.quantity
            if client_cart_item.quantity == user_cart_common_item.quantity
            else client_cart_item.quantity + user_cart_common_item.quantity
        )
        user_cart_common_item.refresh_from_db()
        self.assertEqual(user_cart_common_item.quantity, expected_quantity)
