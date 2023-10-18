from django.test import TestCase

from rest_framework.test import APIClient

class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
