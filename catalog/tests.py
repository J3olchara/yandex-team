"""CATALOG app tests"""

import catalog.models
from django.core import exceptions
from django.db import transaction, utils
from django.db.models.query import QuerySet
from django.test import Client
from django.urls import NoReverseMatch, reverse
from parameterized import parameterized

from . import models

# isort: off
import core  # noqa: I100

# isort: on


class CatalogURLTests(core.tests.SetupData):
    """CATALOG app test cases"""

    APP_DIR = reverse('catalog:catalog')

    def test_catalog_endpoint(self) -> None:
        """test getting response from app dir"""
        response = Client().get(self.APP_DIR)
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_endpoint_and_item_id(self) -> None:
        """test status code 200 from catalog and checking given item_id"""
        item_id = self.item_on_main.id
        test_path = reverse(
            'catalog:int_item_detail', kwargs={'item_id': item_id}
        )
        response = Client().get(test_path)
        self.assertIn(str(item_id).encode(), response.content, test_path)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([[2, -10], [1, 0]])
    def test_re_path(self, test_200: int, test_404: int) -> None:
        """testing regular expression path from catalog"""
        dir_200 = reverse(
            'catalog:re_item_detail', kwargs={'item_id': test_200}
        )
        response = Client().get(dir_200)
        self.assertEqual(response.status_code, 200, test_200)
        self.assertIn(str(test_200).encode(), response.content)
        with self.assertRaises(NoReverseMatch):
            reverse('catalog:re_item_detail', kwargs={'item_id': test_404})

    @parameterized.expand([[2, -10], [1, 0]])
    def test_natnum_converter(self, test_200: int, test_404: int) -> None:
        """tests self written converter for /catalog/converters/<natnum>"""
        dir_200 = reverse(
            'catalog:conv_item_detail', kwargs={'item_id': test_200}
        )
        response = Client().get(dir_200)
        self.assertEqual(response.status_code, 200, test_200)
        self.assertIn(str(test_200).encode(), response.content)
        with self.assertRaises(NoReverseMatch):
            reverse('catalog:conv_item_detail', kwargs={'item_id': test_404})


class CatalogModelTests(core.tests.SetupData):
    """tests valid model working"""

    def test_base_slug_abstract_class(self) -> None:
        """test field validators"""
        with self.assertRaises(exceptions.ValidationError):
            tag = models.Tag(name='1' * 151, slug='test')
            tag.full_clean()
            tag.save()
            tag = models.Tag(name='test', slug='1' * 201)
            tag.full_clean()
            tag.save()
        self.assertEqual(self.tag_published.is_published, True)
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                models.Tag.objects.create(
                    name=self.tag_published.name,
                    slug=self.tag_published.slug,
                )

    def test_category(self) -> None:
        category = models.Category(
            name='test',
            slug='test',
        )
        self.assertEqual(category.weight, 100)

    @parameterized.expand(  # type: ignore[misc]
        [
            ['плохо', 'роскошно'],
            [
                'Роскошный',
                'превосходно',
            ],
            ['роскный', 'Роскошно живём'],
        ]
    )
    def test_item(self, bad_test: str, good_test: str) -> None:
        with self.assertRaises(exceptions.ValidationError):
            item = models.Item(
                name='test',
                text=bad_test,
                category=self.category_published,
                image='test.jpg',
            )
            item.full_clean()
        item = models.Item(
            name='test',
            text=good_test,
            category=self.category_published,
            image='test.jpg',
        )
        item.full_clean()

    @parameterized.expand(  # type: ignore[misc]
        [
            'tеst',
            'Test',
            'test! ,',
            'TESт',
            'tes t',
            ' test ',
        ]
    )
    def test_abstract_base_slug_normalized_name(self, name: str) -> None:
        models.Tag.objects.create(name='test', slug='test')
        with transaction.atomic():
            with self.assertRaises(utils.IntegrityError):
                models.Tag.objects.create(name=name, slug='testslug')
        models.Tag.objects.create(name='test name', slug='testslug')


class CatalogShowTests(core.tests.SetupData):
    """
    Catalog views tests

    tests that user sees only that he is able to see
    """

    def group_query_set(self, qs, field_name, pk):
        return super(CatalogShowTests, self).group_query_set(
            qs, field_name, pk
        )

    def test_catalog_correct_context(self):
        """tests that user have got an items list"""
        test_path = reverse('catalog:catalog')
        response = Client().get(test_path)
        items = self.group_query_set(
            response.context['items'], 'tags__name', 'id'
        )
        self.assertEqual(
            len(items), 3
        )  # is_on_main True, False, False with is_published=True

    def test_item_detail_context(self):
        """tests that user hae got an item detail"""
        item = self.item_on_main
        test_path = reverse(
            'catalog:int_item_detail', kwargs={'item_id': item.id}
        )
        response = Client().get(test_path)
        grouped_item = self.group_query_set(
            response.context['item_raw'], 'tags__name', 'id'
        )[0]
        self.assertEqual(
            grouped_item.keys(),
            {'name', 'text', 'category__name', 'image', 'tags__name', 'id'},
        )

    def test_sql_fields(self):
        items: QuerySet = self.group_query_set(
            catalog.models.Item.objects.published(), 'tags__name', 'id'
        )
        self.assertEqual(
            items[0].keys(),
            {'name', 'text', 'id', 'category__name', 'image', 'tags__name'},
        )

    def test_sql_fields_item_list(self):
        response = Client().get(reverse('catalog:catalog'))
        item = self.group_query_set(
            response.context['items'], 'tags__name', 'id'
        )[0]
        self.assertEqual(
            set(item.keys()),
            {'name', 'text', 'id', 'category__name', 'image', 'tags__name'},
        )

    def test_sql_field_item_detail(self):
        response = Client().get(
            reverse(
                'catalog:int_item_detail',
                kwargs={'item_id': self.item_published.id},
            )
        )
        item = self.group_query_set(
            response.context['item_raw'], 'tags__name', 'id'
        )[0]
        self.assertEqual(
            set(item.keys()),
            {'name', 'text', 'category__name', 'image', 'tags__name', 'id'},
        )
