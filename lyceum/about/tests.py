"""ABOUT app tests"""
from django.test import Client, TestCase


class HomepageURLTests(TestCase):
    """ABOUT app test cases"""

    APP_DIR = '/about/'

    def test_about_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)
