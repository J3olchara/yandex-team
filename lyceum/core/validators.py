"""CORE validators"""
import re

from django.core.exceptions import ValidationError


def slug_validator(value: str) -> None:
    pattern = r'^[1-9a-zA-Z_-]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Slug does not satisfy the requirements'
            '(only consist of nums, english letters, _ and -)'
        )


def rich_text_validator(value: str) -> None:
    value = value.lower()
    if not ('превосходно' in value or 'роскошно' in value):
        raise ValidationError(
            'Text must contain one of words: превосходно или роскошно.'
        )
