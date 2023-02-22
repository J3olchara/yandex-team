"""HOMEPAGE app database models"""
from string import punctuation
from typing import Any

from django.core import validators
from django.db import models

from . import validators as custom_validators


class Base(models.Model):
    is_published: Any = models.BooleanField(
        verbose_name='Опубликован',
        help_text='Да/Нет',
        default=True,
    )
    name: Any = models.CharField(
        verbose_name='Название',
        help_text='Придумайте название',
        max_length=150,
        validators=[
            validators.MaxLengthValidator(150),
        ],
    )

    class Meta:
        abstract = True


class BaseSlug(Base):
    slug: Any = models.CharField(
        verbose_name='Уникальный артикул',
        help_text='Придумайте артикул'
        '(может состоять только из латинских букв, цифр, _ и -)',
        max_length=200,
        unique=True,
        validators=[
            custom_validators.slug_validator,
            validators.MaxLengthValidator(200),
        ],
    )

    normalized_name: Any = models.CharField(
        verbose_name='Нормализованное имя',
        max_length=150,
        unique=True,
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.normalized_name = self.normalize_name()
        return super().save()

    def normalize_name(self) -> str:
        normalized: str = self.name.upper()
        tab = dict.fromkeys(punctuation)
        alphabet = {  # rus: eng
            'А': 'A',
            'В': 'B',
            'Е': 'E',
            'Т': 'T',
            'О': 'O',
            'Р': 'P',
            'Н': 'H',
            'К': 'K',
            'Х': 'X',
            'С': 'C',
            'М': 'M',
            ' ': '',
        }
        tab.update(alphabet)
        translate_tab = str.maketrans(tab)
        return normalized.translate(translate_tab)

    class Meta:
        abstract = True
