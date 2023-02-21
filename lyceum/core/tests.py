from django.core import exceptions
from django.test import TestCase

from . import validators


class ValidatorsTest(TestCase):
    def test_text_validator(self) -> None:
        tests = (
            ('123abc-_[', False),
            ('123abc-_=', False),
            ('123abc-_+', False),
        )
        with self.assertRaises(exceptions.ValidationError):
            for value, _ in tests:
                validators.slug_validator(value)
        validators.slug_validator('123abc-_')

    def test_rich_text(self) -> None:
        tests_good = (
            'превосходно',
            'роскошно',
            'роскошно ест',
        )
        tests_bad = (
            'плохо',
            'роскошный',
            'превосходный',
        )
        with self.assertRaises(exceptions.ValidationError):
            for value in tests_bad:
                validators.rich_text_validator(value)
        for value in tests_good:
            validators.rich_text_validator(value)
