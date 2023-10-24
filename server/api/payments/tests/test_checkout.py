from datetime import datetime, timedelta
from unittest.mock import patch

from django.utils import timezone
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK
from model_bakery import baker

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
        serialized_checkout = CheckoutReadOnlySerializer(checkout)
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
            serialized_checkout = CheckoutReadOnlySerializer(new_checkout)
            self.assertEqual(response.json(), serialized_checkout.data)

            # Validate first checkout is invalid now
            checkout.refresh_from_db()
            self.assertTrue(checkout.is_expired)
