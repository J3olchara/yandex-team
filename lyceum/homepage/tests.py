"""HOMEPAGE app tests"""
from django.test import Client, TestCase


class HomepageURLTests(TestCase):
    """HOMEPAGE app test cases"""

    APP_DIR = '/'

    def test_homepage_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)

    def test_coffee_django(self) -> None:
        """test getting response from app dir"""
        test_path = self.APP_DIR + 'coffee/'
        response = Client().get(test_path)
        self.assertEqual(response.status_code, 418)
        self.assertIn(
            bytes('Я чайник', 'utf-8'),
            response.content,
            response.content.decode(),
        )
