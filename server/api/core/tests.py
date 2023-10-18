from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from model_bakery import baker

from core.test import BaseTestCase



class SecurityTests(BaseTestCase):
    pass
    # def test_csrf_token(self) -> None:
    #     from rest_framework.test import APIClient
    #     self.client = APIClient(enforce_csrf_checks=True)
    #     user = baker.make(get_user_model())
    #     self.client.force_login(user)
    #     url = reverse("core:csrf-test")
    #     response = self.client.post(url)
    #     print(response.status_code, response.content)