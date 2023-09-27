import re

from django.core import mail
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory
from model_bakery import baker


class TestRegistration(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    # @override_settings(EMAIL_BACKEND='django.core.mail.backends.filebased.EmailBackend')
    def test_user_register(self) -> None:
        URL = reverse("accounts:api-root")

        email = "someuser@gmail.com"
        payload = {
            "email": email,
            "password": "verystrongpassword",
            "re_password": "verystrongpassword"
        }
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            get_user_model().objects.filter(email=email).exists()
        )

    def test_user_register_with_username_returns_http400(self) -> None:
        URL = reverse("accounts:api-root")

        username = "testuser"
        payload = {
            "username": username,
            "email": "",
            "password": "verystrongpassword",
            "re_password": "verystrongpassword"
        }
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 400)


class TestPasswordRecovery(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    # @override_settings(EMAIL_BACKEND="django.core.mail.backends.filebased.EmailBackend")
    def test_password_reset(self) -> None:
        URL = reverse("accounts:accounts-reset-password")

        user = baker.make(get_user_model())
        payload = {"email": user.email} # type: ignore
        response = self.client.post(URL, payload)

        self.assertEqual(response.status_code, 204) # Password reset email is sent

        # Get UID and Token from email body
        pattern = r"\/([^\/]+)\/([^\/]+)\/$"

        mail_body = mail.outbox[0].body
        search = re.search(pattern, mail_body)

        if not search:
            raise Exception("Email not found")
        
        uid, token = search.group(1), search.group(2)

        # Perform password reset operation
        URL = reverse("accounts:accounts-reset-password-confirm")
        password = "verystrongpassword91"
        payload = {
            "uid": uid,
            "token": token,
            "new_password": password,
            "re_new_password": password
        }
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 204)

        # Validate
        user.refresh_from_db()
        self.assertTrue(user.check_password(password))