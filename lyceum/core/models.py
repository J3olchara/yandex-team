"""HOMEPAGE app database models"""
from django.core import validators
from django.db import models

from . import validators as custom_validators


class Base(models.Model):
    is_published = models.BooleanField(
        verbose_name='Опубликован',
        help_text='Да/Нет',
        default=True,
    )
    name = models.CharField(
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
    slug = models.CharField(
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

    class Meta:
        abstract = True
