from django.test import TestCase, Client

class BaseTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
