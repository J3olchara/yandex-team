"""CORE validators"""
import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def slug_validator(value: str) -> None:
    pattern = re.compile(r'^[1-9a-zA-Z_-]+$')
    if not re.match(pattern, value):
        raise ValidationError(
            'Slug does not satisfy the requirements'
            '(only consist of nums, english letters, _ and -)'
        )


@deconstructible
class ValidateMustContain:
    def __init__(self, *words: str) -> None:
        self.words = words

    def __call__(self, value: str) -> None:
        value = value.lower()
        fl = (word not in value for word in self.words)
        if all(fl):
            raise ValidationError(
                f'Text must contain one of words: {self.words}'
            )
