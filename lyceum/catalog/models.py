"""CATALOG app database models"""
from django.db import models
import Core


class Tag(Core.models.BaseSlug):
    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name[:15]


class Category(Core.models.BaseSlug):
    weight = models.PositiveSmallIntegerField(
        verbose_name='Вес',
        default=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:15]


class Item(Core.models.Base):
    text = models.TextField(
        'Описание',
        help_text='Опишите объект',
        validators=[
            Core.validators.rich_text_validator,
        ]
    )

    category = models.ForeignKey(
        'category',
        on_delete=models.DO_NOTHING,
    )

    tags = models.ManyToManyField(Tag)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name[:15]
