from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from model_bakery import baker


class TestAuthentication(TestCase):
    def setUp(self) -> None:
        self.client = Client()


    def test_login(self) -> None:
        """
        Test successful user login
        """
        URL = reverse("accounts:login")
        user = baker.make(get_user_model())
        user_password = "12345678"
        user.set_password(user_password)
        user.save()

        payload = {
            "email": user.email, # type: ignore
            "password": user_password
        }
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 200)
        token = response.json()["auth_token"]

        self.assertTrue(
            Token.objects.filter(key=token, user=user).exists()
        )

    def test_login_with_username_returns_http400(self) -> None:
        """
        `USERNAME_FIELD` is set to email, user shouldn't be able to login using username
        """
        URL = reverse("accounts:login")
        user = baker.make(get_user_model())
        user_password = "12345678"
        user.set_password(user_password)
        user.save()

        payload = {
            "username": user.username, # type: ignore
            "password": user_password
        }
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_logout(self) -> None:
        """
        Test user logout success
        """
        URL = reverse("accounts:login")
        user = baker.make(get_user_model())
        user_password = "12345678"
        user.set_password(user_password)
        user.save()

        # Login user through endpoint
        payload = {
            "email": user.email, # type: ignore
            "password": user_password
        }
        response = self.client.post(URL, payload)
        self.assertTrue(Token.objects.filter(user=user).exists())
        token = response.json()["auth_token"]

        # Perform logout, token should be deleted
        URL = reverse("accounts:logout")
        headers = {"Authorization": f"Token {token}"}
        response = self.client.post(URL, headers=headers) # type: ignore
        
        self.assertEqual(response.status_code, 204)        
        self.assertFalse(Token.objects.filter(user=user).exists())

    def test_change_password(self) -> None:
        """
        Test user change password success
        """
        URL = reverse("accounts:accounts-set-password")
        current_password = "12345678"
        user = baker.make(get_user_model())
        user.set_password(current_password)
        user.save()

        token = Token.objects.create(user=user)
        new_password = "verystrongnewpassword"

        payload = {
            "new_password": new_password,
            "re_new_password": new_password,
            "current_password": current_password
        }
        headers = {"Authorization": f"Token {token}"}
        response = self.client.post(URL, payload, headers=headers) # type: ignore
        self.assertEqual(response.status_code, 204)

        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))
