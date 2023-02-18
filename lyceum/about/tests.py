"""ABOUT app tests"""
from django.test import Client, TestCase
from django.urls import reverse


class HomepageURLTests(TestCase):
    """ABOUT app test cases"""

    def test_about_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(reverse('about'))
        self.assertEqual(response.status_code, 200)
