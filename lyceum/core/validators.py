"""CORE validators"""
import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


def slug_validator(value: str) -> None:
    pattern = r'^[1-9a-zA-Z_-]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Slug does not satisfy the requirements'
            '(only consist of nums, english letters, _ and -)'
        )


# def ValidateMustContain(*words) -> '(value: str) -> None':
#     def wrapper(value: str) -> None:
#         value = value.lower()
#         fl = [word in value for word in words]
#         if not any(fl):
#             raise ValidationError(
#                 f'Text must contain one of words: {words}'
#             )
#     return wrapper


@deconstructible
class ValidateMustContain:
    def __init__(self, *words: str) -> None:
        self.words = words

    def __call__(self, value: str) -> None:
        value = value.lower()
        fl = [word in value for word in self.words]
        if not any(fl):
            raise ValidationError(
                f'Text must contain one of words: {self.words}'
            )
