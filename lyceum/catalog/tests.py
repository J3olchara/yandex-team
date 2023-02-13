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
        self.assertIn(
            bytes(item_id, 'utf-8'), response.content, response.content
        )
        self.assertEqual(response.status_code, 200)

    def test_re_path(self):
        """testing regular expression path from catalog"""
        test_path = self.APP_DIR + 're/'
        test_paths_200 = [10, 1]
        test_paths_404 = [-10, 0]
        for item_id_req in test_paths_200:
            response = Client().get(f'{test_path}{item_id_req}/')
            self.assertEqual(response.status_code, 200, item_id_req)
            self.assertIn(str(item_id_req).encode(), response.content)
        for item_id_req in test_paths_404:
            response = Client().get(f'{test_path}{item_id_req}/')
            self.assertEqual(response.status_code, 404, item_id_req)

    def test_natnum_converter(self):
        """tests self written converter for /catalog/converters/<natnum>"""
        test_path = self.APP_DIR + 'converter/'
        test_paths_200 = [10, 1]
        test_paths_404 = [-10, 0]
        for item_id_req in test_paths_200:
            response = Client().get(f'{test_path}{item_id_req}/')
            item_id = response.resolver_match.kwargs['item_id']
            self.assertEqual(response.status_code, 200, item_id_req)
            self.assertEqual(item_id, item_id_req)
        for item_id_req in test_paths_404:
            response = Client().get(f'{test_path}{item_id_req}/')
            self.assertEqual(response.status_code, 404, item_id_req)
