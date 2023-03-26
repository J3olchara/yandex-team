"""HOMEPAGE app tests"""
import core
from django.test import Client, TestCase
from django.urls import reverse


class HomepageURLTests(TestCase):
    """HOMEPAGE app test cases"""

    APP_DIR = reverse('home:home')

    def test_homepage_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)

    def test_coffee_django(self) -> None:
        """test getting response from app dir"""
        test_path = reverse('home:coffee')
        response = Client().get(test_path)
        self.assertEqual(response.status_code, 418)
        self.assertIn(
            bytes('Я чайник', 'utf-8'),
            response.content,
            response.content.decode(),
        )


class CatalogShowTests(core.tests.SetupData):
    """
    Catalog views tests

    tests that user sees only that he is able to see
    """

    def test_home_page_correct_context(self):
        """tests that user have got an items list"""
        test_path = reverse('home:home')
        response = Client().get(test_path)
        self.assertIn('items', response.context)
