"""HOMEPAGE app tests"""
from django.test import Client, TestCase


class HomepageURLTests(TestCase):
    """HOMEPAGE app test cases"""

    APP_DIR = '/'

    def test_homepage_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)
