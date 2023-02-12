"""CATALOG app tests"""
from django.test import Client, TestCase


class HomepageURLTests(TestCase):
    """CATALOG app test cases"""

    APP_DIR = '/catalog/'

    def test_catalog_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_endpoint_and_item_id(self) -> None:
        """test status code 200 from catalog and checking given item_id"""
        item_id = '10'
        test_path = self.APP_DIR + item_id + '/'
        response = Client().get(test_path)
        self.assertIn(bytes(item_id, 'utf-8'), response.content)
        self.assertEqual(response.status_code, 200)
