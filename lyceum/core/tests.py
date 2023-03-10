"""Some tests for Core App"""
import shutil
from typing import Any, List

from django.conf import settings
from django.core import exceptions
from django.db.models import QuerySet
from django.test import TestCase
from parameterized import parameterized

from . import validators


class SetupData(TestCase):
    """
    Setup data for tests
    """

    def setUp(self) -> None:
        from catalog import models

        test_original_file_path = (
            settings.STATICFILES_DIRS_DEV_DIR / 'test_img' / 'nya.jpg'
        )
        test_image_path = str(settings.MEDIA_ROOT / 'test_media_file.jpg')
        shutil.copy2(test_original_file_path, test_image_path)
        self.category_published = models.Category.objects.create(
            name='test_category_published',
            slug='test_category_slug_published',
        )
        self.category_unpublished = models.Category.objects.create(
            is_published=False,
            name='test_category_unpublished',
            slug='test_category_slug_unpublished',
        )
        self.tag_published = models.Tag.objects.create(
            name='test_tag_published',
            slug='test_tag_slug_published',
        )
        self.tag_unpublished = models.Tag.objects.create(
            is_published=False,
            name='test_tag_unpublished',
            slug='test_tag_slug_unpublished',
        )
        self.item_published = models.Item.objects.create(
            name='test_name_published',
            text='some_test_text роскошно',
            image=test_image_path,
            category=self.category_published,
        )
        self.item_published.tags.add(self.tag_unpublished)
        self.item_published.tags.add(self.tag_published)
        self.item_unpublished = models.Item.objects.create(
            is_published=False,
            name='test_name_unpublished',
            text='some_test_text роскошно',
            image=test_image_path,
        )
        self.item_unpublished.tags.add(self.tag_unpublished)
        self.item_unpublished.tags.add(self.tag_published)
        self.item_on_main = models.Item.objects.create(
            is_on_main=True,
            name='test_name_on_main',
            text='some_test_text роскошно',
            image=test_image_path,
            category=self.category_published,
        )
        self.item_on_main.tags.add(self.tag_unpublished)
        self.item_on_main.tags.add(self.tag_published)
        self.item_not_on_main = models.Item.objects.create(
            name='test_name_published_not_on_main',
            text='some_test_text роскошно',
            image=test_image_path,
            category=self.category_unpublished,
        )
        self.item_not_on_main.tags.add(self.tag_unpublished)
        self.item_not_on_main.tags.add(self.tag_published)
        self.image = models.PhotoGallery.objects.create(
            image=test_image_path,
            item=self.item_published,
        )
        self.image = models.PhotoGallery.objects.create(
            image=test_image_path,
            item=self.item_unpublished,
        )
        self.image = models.PhotoGallery.objects.create(
            image=test_image_path,
            item=self.item_on_main,
        )
        self.image = models.PhotoGallery.objects.create(
            image=test_image_path,
            item=self.item_not_on_main,
        )

        self.category_published.clean()
        self.category_published.save()
        self.category_unpublished.clean()
        self.category_unpublished.save()

        self.tag_unpublished.clean()
        self.tag_unpublished.save()
        self.tag_published.clean()
        self.tag_published.save()

        self.item_published.clean()
        self.item_published.save()
        self.item_unpublished.clean()
        self.item_unpublished.save()
        self.item_on_main.clean()
        self.item_on_main.save()
        self.item_not_on_main.clean()
        self.item_not_on_main.save()

        self.image.clean()
        self.image.save()
        return super(SetupData, self).setUp()

    def group_query_set(
        self, qs: QuerySet[Any], field_name: str, pk: str
    ) -> List[Any]:
        j = 0
        i = 0
        grouped = []
        if len(qs):
            grouped.append(qs[0])
            grouped[j][field_name] = [
                grouped[j][field_name],
            ]
            while i < len(qs) - 1:
                if qs[i][pk] != qs[i + 1][pk]:
                    grouped.append(qs[i + 1])
                    grouped[j][field_name] = [
                        qs[i + 1][field_name],
                    ]
                    j += 1
                else:
                    grouped[j - 1][field_name].append(qs[i + 1][field_name])
                i += 1
        return grouped


class ValidatorsTest(TestCase):
    validator_test_words = ['роскошно', 'превосходно']

    @parameterized.expand(  # type: ignore[misc]
        [
            ('123abc-_[', '123abc-_'),
            ('123abc-_=', 'abc-_'),
            ('123abc-_+', '1bc'),
        ]
    )
    def test_text_validator(self, bad_test: str, good_test: str) -> None:
        with self.assertRaises(exceptions.ValidationError):
            validators.slug_validator(bad_test)
        validators.slug_validator(good_test)

    @parameterized.expand(  # type: ignore[misc]
        [
            ['превосходно', 'плохо'],
            ['роскошно', 'роскошный'],
            ['роскошно ест', 'превосходный'],
        ]
    )
    def test_rich_text_good(self, test_good: str, test_bad: str) -> None:
        with self.assertRaises(exceptions.ValidationError):
            validators.ValidateMustContain(*self.validator_test_words)(
                test_bad
            )
        validators.ValidateMustContain(*self.validator_test_words)(test_good)
