from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from model_bakery import baker


class TestAuthentication(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_signin(self) -> None:
        """
        Test successful user signin
        """
        URL = reverse("accounts:user-signin")
        user = baker.make(get_user_model())
        user_password = "12345678"
        user.set_password(user_password)
        user.save()

        payload = {"email": user.email, "password": user_password}  # type: ignore
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 200)

        # self.assertTrue(
        #     Token.objects.filter(key=token, user=user).exists()
        # )

    def test_signin_with_username_returns_http400(self) -> None:
        """
        `USERNAME_FIELD` is set to email, user shouldn't be able to signin using username
        """
        URL = reverse("accounts:user-signin")
        user = baker.make(get_user_model())
        user_password = "12345678"
        user.set_password(user_password)
        user.save()

        payload = {"username": user.username, "password": user_password}  # type: ignore
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 400)
        # self.assertFalse(Token.objects.filter(user=user).exists())

    def test_signout(self) -> None:
        """
        Test user signout success
        """
        URL = reverse("accounts:user-signin")
        user = baker.make(get_user_model())
        user_password = "12345678"
        user.set_password(user_password)
        user.save()

        # signin user through endpoint
        payload = {"email": user.email, "password": user_password}  # type: ignore
        response = self.client.post(URL, payload)
        self.assertEqual(response.status_code, 200)

        # Perform signout, token should be deleted
        URL = reverse("accounts:user-signout")
        response = self.client.post(URL)  # type: ignore

        self.assertEqual(response.status_code, 204)

    def test_change_password(self) -> None:
        """
        Test user change password success
        """
        URL = reverse("accounts:accounts-set-password")
        current_password = "12345678"
        user = baker.make(get_user_model())
        user.set_password(current_password)
        user.save()

        new_password = "verystrongnewpassword"

        payload = {
            "new_password": new_password,
            "re_new_password": new_password,
            "current_password": current_password,
        }
        self.client.force_login(user)
        response = self.client.post(URL, payload)  # type: ignore
        self.assertEqual(response.status_code, 204)

        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))
