"""CATALOG app database models"""
from typing import Any

# isort: off

import core

from django.db import models

# isort: on


class Tag(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """TAG model for Item"""

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self) -> Any:
        return self.name[:20]


class Category(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """CATEGORY model for Item"""

    weight: Any = models.PositiveSmallIntegerField(
        verbose_name='вес', default=100
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> Any:
        return self.name[:40]


class Item(core.models.Base):  # type: ignore[name-defined, misc]
    """Object from the catalog model"""

    text: Any = models.TextField(
        verbose_name='описание',
        help_text='Опишите объект',
        validators=[
            core.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )

    category: Any = models.ForeignKey(
        'category',
        verbose_name='категория',
        help_text='Выберите категорию',
        on_delete=models.SET_NULL,
        null=True,
    )

    tags: Any = models.ManyToManyField(
        Tag,
        verbose_name='тэги',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> Any:
        return self.name[:15]
