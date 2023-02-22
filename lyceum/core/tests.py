from django.core import exceptions
from django.test import TestCase

from parameterized import parameterized

from . import validators


class ValidatorsTest(TestCase):

    validator_test_words = ['роскошно', 'превосходно']

    @parameterized.expand([
            ('123abc-_[', '123abc-_'),
            ('123abc-_=', 'abc-_'),
            ('123abc-_+', '1bc'),
        ])
    def test_text_validator(self, bad_test, good_test) -> None:
        with self.assertRaises(exceptions.ValidationError):
            validators.slug_validator(bad_test)
        validators.slug_validator(good_test)

    @parameterized.expand([
            ['превосходно', 'плохо'],
            ['роскошно', 'роскошный'],
            ['роскошно ест', 'превосходный'],
    ])
    def test_rich_text_good(self, test_good, test_bad) -> None:
        with self.assertRaises(exceptions.ValidationError):
            validators.ValidateMustContain(*self.validator_test_words)(test_bad)
        validators.ValidateMustContain(*self.validator_test_words)(test_good)
