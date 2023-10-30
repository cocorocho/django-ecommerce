from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from cities_light.models import Country, Region
from model_bakery import baker

from payments.models import Address
from payments.constants import CHECKOUT_EXPIRE_AGE
from payments.serializers.checkout import CheckoutReadOnlySerializer
from core.test import BaseTestCase


class TestCheckoutQuerySet(BaseTestCase):
    def test_valid_queryset(self) -> None:
        checkout = baker.make_recipe("payments.tests.checkout")

        with patch("django.utils.timezone.now") as mock_timezone_now:
            valid_dt = datetime.now(tz=timezone.get_current_timezone()) + timedelta(
                seconds=(CHECKOUT_EXPIRE_AGE - 50)
            )
            mock_timezone_now.return_value = valid_dt
            # Before expire date, not expired, is valid
            self.assertFalse(checkout.is_expired)
            # Test queryset `objects.valid`
            self.assertEqual(checkout._meta.model.objects.valid().count(), 1)

            # Expired
            invalid = datetime.now(tz=timezone.get_current_timezone()) + timedelta(
                seconds=CHECKOUT_EXPIRE_AGE
            )
            mock_timezone_now.return_value = invalid
            self.assertTrue(checkout.is_expired)
            # Test queryset `objects.valid`
            self.assertEqual(checkout._meta.model.objects.valid().count(), 0)


class TestCheckoutEndpoints(BaseTestCase):
    def test_checkout_cart(self) -> None:
        cart = baker.make_recipe("store.tests.cart")

        url = reverse("payments:checkout-create")

        payload = {"cart_session_id": cart.session_id}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_200_OK)
        checkout = cart.checkouts.first()

        # Annotate fields
        queryset = (
            checkout._meta.model.objects.with_checkout_data().with_cart_relations()
        )
        checkout = queryset.get(pk=checkout.pk)

        serialized_checkout = CheckoutReadOnlySerializer(checkout)
        data = serialized_checkout.data
        data["cart"] = dict(data["cart"])
        self.assertEqual(response.json(), serialized_checkout.data)

        # Test create new checkout when checkout expires
        with patch("django.utils.timezone.now") as mock_timezone_now:
            dt = datetime.now(tz=timezone.get_current_timezone()) + timedelta(
                seconds=CHECKOUT_EXPIRE_AGE
            )
            mock_timezone_now.return_value = dt

            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, HTTP_200_OK)
            self.assertEqual(
                cart.checkouts.count(), 2
            )  # because first was invalid after `CHECKOUT_EXPIRE_AGE`
            new_checkout = cart.checkouts.latest("pk")

            # Get queryset for annotations
            queryset = (
                new_checkout._meta.model.objects.with_checkout_data().with_cart_relations()
            )
            new_checkout = queryset.get(pk=new_checkout.pk)
            serialized_checkout = CheckoutReadOnlySerializer(new_checkout)
            self.assertEqual(response.data, serialized_checkout.data)

            # Validate first checkout is invalid now
            checkout.refresh_from_db()
            self.assertTrue(checkout.is_expired)

    def test_finalize_checkout_as_guest(self) -> None:
        """
        Finalize checkout and create the order
        """
        country = Country.objects.create(name="Turkey", slug="turkey")
        region = Region.objects.create(name="antalya", slug="antalya", country=country)

        ### Create new checkout ###
        cart = baker.make_recipe("store.tests.cart")
        cart_items = baker.make_recipe("store.tests.cart_item", cart=cart, _quantity=5)

        url = reverse("payments:checkout-create")
        payload = {"cart_session_id": cart.session_id}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        token = response.data["token"]
        checkout = cart.checkouts.get(token=token)
        ###########################

        url = reverse("payments:checkout-finalize", args=(checkout.token,))

        # Guest user, buy without logging-in
        payload = {
            "email": "test@example.com",
            "shipping_address": {
                "country": "turkey",
                "city": "antalya",
                "postal_code": "123456",
                "address": "test st. abc blv. 11/23",
                "phone": "",
            },
            "payment": {"use_shipping_address_as_billing_address": True},
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_finalize_checkout_as_logged_in_user(self) -> None:
        country = Country.objects.create(name="Turkey", slug="turkey")
        region = Region.objects.create(name="antalya", slug="antalya", country=country)

        ### Create new checkout ###
        user = baker.make(get_user_model())
        self.client.force_login(user)
        cart = baker.make_recipe("store.tests.cart")
        cart_items = baker.make_recipe("store.tests.cart_item", cart=cart, _quantity=5)

        url = reverse("payments:checkout-create")
        payload = {"cart_session_id": cart.session_id}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 200)
        token = response.data["token"]
        checkout = cart.checkouts.get(token=token)
        ###########################

        user_address = baker.make(Address, user=user, country=country, city=region)

        url = reverse("payments:checkout-finalize", args=(checkout.token,))
        payload = {
            # Email is not required
            "shipping_address": None,
            "shipping_address_id": user_address.id,
            "payment": {"use_shipping_address_as_billing_address": True},
        }

        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
