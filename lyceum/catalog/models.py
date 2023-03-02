"""CATALOG app database models"""
from typing import Any

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.html import mark_safe  # type: ignore[attr-defined]
from django_cleanup import cleanup
from sorl.thumbnail import get_thumbnail

# isort: off
import core  # noqa: I100

# isort: on


class Tag(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """
    TAG model for Item

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item
    slug: char[200]. Explains unique item/post ID
    normalized_name: char[150]. Normalized name field
        without registry, punctuation and other.
        auto-creates from name field.
    """

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'

    def __str__(self) -> Any:
        return self.name[:20]


class Category(core.models.BaseSlug):  # type: ignore[name-defined, misc]
    """
    CATEGORY model for Item

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item
    slug: char[200]. Explains unique item/post ID
    normalized_name: char[150]. Normalized name field
        without registry, punctuation and other.
        auto-creates from name field.
    weight: Item weight field (0 -> 32768)
    """

    weight: Any = models.PositiveSmallIntegerField(
        verbose_name='вес', default=100
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> Any:
        return self.name[:40]


class PhotoGallery(models.Model):
    """
    PhotoGallery Model for Item

    image: second-needed image for gallery
    item: FK to Item that uses this image

    """

    image: Any = models.ImageField(
        verbose_name='фото',
        help_text='Загрузите фото',
        upload_to='uploads/gallery/',
    )

    item: Any = models.ForeignKey('Item', on_delete=models.CASCADE, blank=True)

    def get_image_px(
        self, px: str = '400x300', crop: str = 'center', quality: int = 51
    ) -> Any:
        """
        crops the picture

        px: string. format of the new image (1200x400, 1200)
        crop: string. crop centering
        quality: integer. quality of the new image
        """
        return get_thumbnail(self.image, px, crop=crop, quality=quality)

    def image_tmb(self) -> Any:
        """returns HTML picture for Item"""
        return mark_safe(f'<img src="{self.image.url}" width="50">')

    def __str__(self) -> str:
        return str(self.image.url)

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'


@cleanup.select
class Item(core.models.Base):  # type: ignore[name-defined, misc]
    """
    Item database object

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item
    text: string. Explains item description.
        Must contain one from words: 'превосходно' or 'роскошно'.
    category: FK to Category. Explains item category
        like kitchen instrument or something else.
    main_image: ImageFile. Main Item picture that user firstly see in catalog
    """

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

    main_image: Any = models.ImageField(
        verbose_name='основное фото',
        help_text='Выберите основное фото товара',
    )

    def image_tmb(self) -> Any:
        if self.main_image:
            return mark_safe(f'<img src="{self.main_image.url}" width="50">')
        return 'Изображения нет'

    def full_clean(self):
        return super(Item, self).full_clean()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> Any:
        return self.name[:15]
