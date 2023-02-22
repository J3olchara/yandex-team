"""CATALOG app tests"""

from django.core import exceptions
from django.db import transaction, utils
from django.test import Client, TestCase
from django.urls import reverse

from . import models


class CatalogURLTests(TestCase):
    """CATALOG app test cases"""

    APP_DIR = reverse('catalog')

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

    def test_re_path(self) -> None:
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

    def test_natnum_converter(self) -> None:
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


class CatalogModelTests(TestCase):
    """tests valid model working"""

    def test_base_slug_abstract_class(self) -> None:
        """test field validators"""
        with self.assertRaises(exceptions.ValidationError):
            self.tag = models.Tag(name='1' * 151, slug='test')
            self.tag.full_clean()
            self.tag.save()
            self.tag = models.Tag(name='test', slug='1' * 201)
            self.tag.full_clean()
            self.tag.save()
        self.tag = models.Tag(name='test', slug='test')
        self.assertEqual(self.tag.is_published, True)
        self.tag.save()
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                models.Tag.objects.create(
                    name='test',
                    slug='test',
                )

    def test_category(self) -> None:
        self.category = models.Category(
            name='test',
            slug='test',
        )
        self.assertEqual(self.category.weight, 100)

    def test_item(self) -> None:
        bad_tests = (
            'плохо',
            'Роскошный',
            'роскный',
        )
        good_tests = ('роскошно', 'превосходно', 'Роскошно живём')
        self.category = models.Category.objects.create(
            name='test',
            slug='test',
        )
        with self.assertRaises(exceptions.ValidationError):
            for text in bad_tests:
                self.item = models.Item(
                    name='test', text=text, category=self.category
                )
                self.item.full_clean()
        for text in good_tests:
            self.item = models.Item(
                name='test', text=text, category=self.category
            )
            self.item.full_clean()

    def test_abstract_base_slug_normalized_name(self) -> None:
        models.Tag.objects.create(name='test', slug='test')
        test_names = ('tеst', 'Test', 'test! ,', 'TESт', 'tes t', ' test ')
        for name in test_names:
            with transaction.atomic():
                with self.assertRaises(utils.IntegrityError):
                    models.Tag.objects.create(name=name, slug='testslug')
        models.Tag.objects.create(name='test name', slug='testslug')
