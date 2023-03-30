"""
Core models

Contains abstract models for another apps
"""
from typing import Any, Dict, Optional, Union

from django.core import validators
from django.db import models
from django.utils.html import SafeString  # type: ignore[attr-defined]
from django.utils.html import mark_safe  # type: ignore[attr-defined]
from sorl.thumbnail import get_thumbnail

from core import support
from core import validators as custom_validators


class Base(models.Model):
    """
    BASE Abstract class for posts, items and other

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item
    """

    is_published: Union[
        bool, 'models.BooleanField[Any, Any]'
    ] = models.BooleanField(
        verbose_name='опубликован',
        help_text='Да/Нет',
        default=True,
    )
    name: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
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

    slug: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
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

    normalized_name: Union[
        str, 'models.CharField[Any, Any]'
    ] = models.CharField(
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


class Image(models.Model):
    """
    PhotoGallery Model for Item

    image: second-needed image for gallery
    item: FK to Item that uses this image

    """

    image: 'models.ImageField' = models.ImageField(
        verbose_name='фото',
        help_text='Загрузите фото',
        upload_to=support.get_upload_location,
        max_length=200,
    )

    def get_image_px(
        self, px: str = '300x400', crop: str = 'center', quality: int = 70
    ) -> Any:
        """
        crops the picture

        px: string. format of the new image (1200x400, 1200)
        crop: string. crop centering
        quality: integer. quality of the new image
        """
        return get_thumbnail(self.image, px, crop=crop, quality=quality)

    def image_tmb(self) -> Union[SafeString, Any]:
        """returns HTML picture for Item"""
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="50">')
        return mark_safe('Изображения нет')

    def __str__(self) -> str:
        return str(self.image.url)

    class Meta:
        abstract = True
