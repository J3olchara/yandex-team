"""CATALOG app database models"""
from typing import Any

import core  # isort: skip

from django.db import models


class Tag(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """TAG model for Item"""

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self) -> Any:
        return self.name[:20]


class Category(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """CATEGORY model for Item"""

    weight = models.PositiveSmallIntegerField(verbose_name='Вес', default=100)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> Any:
        return self.name[:40]


class Item(core.models.Base):  # type: ignore[name-defined, misc]
    """Object from the catalog model"""

    text = models.TextField(
        'Описание',
        help_text='Опишите объект',
        validators=[
            core.validators.rich_text_validator,
        ],
    )

    category = models.ForeignKey(
        'category',
        verbose_name='Категория',
        help_text='Выберите категорию',
        on_delete=models.DO_NOTHING,
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self) -> Any:
        return self.name[:15]
