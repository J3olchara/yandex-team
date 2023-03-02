"""HOMEPAGE app database models"""
from typing import Any, Dict, Optional

from django.core import validators
from django.db import models

from . import support
from . import validators as custom_validators


class Base(models.Model):
    """
    BASE Abstract class for posts, items and other

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item

    """

    is_published: Any = models.BooleanField(
        verbose_name='опубликован',
        help_text='Да/Нет',
        default=True,
    )
    name: Any = models.CharField(
        verbose_name='название',
        help_text='Придумайте название',
        max_length=150,
        validators=[
            validators.MaxLengthValidator(150),
        ],
    )

    class Meta:
        abstract = True


class BaseSlug(Base):
    """
    BASESlug Abstract class for tags, categories and other

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item
    slug: char[200]. Explains unique item/post ID
    normalized_name: char[150]. Normalized name field
        without registry, punctuation and other.
        auto-creates from name field.

    """

    slug: Any = models.CharField(
        verbose_name='уникальный артикул',
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
        verbose_name='нормализованное имя',
        max_length=150,
        unique=True,
        editable=False,
    )

    normalizer_alphabet: Dict[
        str, Optional[Any]
    ] = support.get_normalize_table()

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.normalized_name = self.normalize_name()
        return super().save()

    def normalize_name(self) -> str:
        normalized: str = self.name.upper()
        translate_tab = str.maketrans(self.normalizer_alphabet)
        return normalized.translate(translate_tab)

    class Meta:
        abstract = True
