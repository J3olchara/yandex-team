"""CATALOG app database models"""
from typing import Any

# isort: off

import core

from django.db import models

# isort: on


class Tag(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """TAG model for Item"""

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> Any:
        return self.name[:20]


class Category(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """CATEGORY model for Item"""

    weight: Any = models.PositiveSmallIntegerField(
        verbose_name='Вес', default=100
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> Any:
        return self.name[:40]


class Item(core.models.Base):  # type: ignore[name-defined, misc]
    """Object from the catalog model"""

    text: Any = models.TextField(
        'Описание',
        help_text='Опишите объект',
        validators=[
            core.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )

    category: Any = models.ForeignKey(
        'category',
        verbose_name='Категория',
        help_text='Выберите категорию',
        on_delete=models.DO_NOTHING,
    )

    tags: Any = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> Any:
        return self.name[:15]
