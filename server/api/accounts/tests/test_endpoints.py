from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework.reverse import reverse
from model_bakery import baker


class TestUsersEndpoints(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_djoser_list_users_endpoint(self) -> None:
        URL = reverse("accounts:accounts-list")
        user = baker.make(get_user_model())

        self.client.force_login(user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 404)
        