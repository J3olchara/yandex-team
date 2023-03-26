"""ABOUT app tests"""
from django.test import Client, TestCase
from django.urls import reverse


class HomepageURLTests(TestCase):
    """ABOUT app test cases"""

    APP_DIR = reverse('about:about')

    def test_about_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)
