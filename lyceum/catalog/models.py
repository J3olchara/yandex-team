"""CATALOG app database models"""
from typing import Any

import core  # noqa: I100
from ckeditor.fields import RichTextField
from django.db import models
from django.utils.html import mark_safe  # type: ignore[attr-defined]
from django_cleanup import cleanup
from sorl.thumbnail import get_thumbnail


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


class MainImage(models.Model):  # type: ignore[django-manager-missing]
    image: Any = models.ImageField(
        verbose_name='Фото',
        help_text='Загрузите фото',
        upload_to='uploads/main_images/',
    )

    def get_image_px(
        self, px: str = '400x300', crop: str = 'center', quality: int = 51
    ) -> Any:
        return get_thumbnail(self.image, px, crop=crop, quality=quality)

    def image_tmb(self) -> Any:
        return mark_safe(
            f'<img src="{self.image.url}" width="16" height="16">'
        )

    def __str__(self) -> str:
        return str(self.image.url)

    class Meta:
        verbose_name = 'Главное изображение'
        verbose_name_plural = 'Главные изображения'


class PhotoGallery(models.Model):  # type: ignore[django-manager-missing]
    image: Any = models.ImageField(
        verbose_name='Фото',
        help_text='Загрузите фото',
        upload_to='uploads/gallery/',
    )

    def get_image_px(
        self, px: str = '400x300', crop: str = 'center', quality: int = 51
    ) -> Any:
        return get_thumbnail(self.image, px, crop=crop, quality=quality)

    def image_tmb(self) -> Any:
        return mark_safe(f'<img src="{self.image.url}" width="50">')

    def __str__(self) -> str:
        return str(self.image.url)

    class Meta:
        verbose_name = 'Галерея'


@cleanup.select
class Item(core.models.Base):  # type: ignore[name-defined, misc]
    """Object from the catalog model"""

    text: Any = RichTextField(
        verbose_name='описание',
        help_text='Опишите объект',
        validators=[
            core.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )

    category: Any = models.ForeignKey(
        'Category',
        verbose_name='категория',
        help_text='Выберите категорию',
        on_delete=models.SET_NULL,
        null=True,
    )

    tags: Any = models.ManyToManyField(
        'Tag',
        verbose_name='тэги',
    )

    main_image: Any = models.ForeignKey(
        MainImage,
        verbose_name='основное фото',
        help_text='Выберите основное фото, '
        'для загрузки перейдите в таблицу Главные изображения',
        on_delete=models.CASCADE,
    )

    item_gallery: Any = models.ManyToManyField(
        'PhotoGallery',
        verbose_name='галерея',
    )

    def image_tmb(self) -> Any:
        if self.main_image:
            return mark_safe(
                f'<img src="{self.main_image.image.url}" width="50">'
            )
        return 'Изображения нет'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> Any:
        return self.name[:15]
