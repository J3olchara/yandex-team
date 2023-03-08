"""
Database models from Catalog app

There is models that helping users to get information from catalog
like items descriptions, items, their tags, categories and other
"""
from typing import Any, Union

from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import QuerySet
from django_cleanup import cleanup

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

    weight: 'models.PositiveSmallIntegerField[Any, Any]' = (
        models.PositiveSmallIntegerField(verbose_name='вес', default=100)
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self) -> Any:
        return self.name[:40]


@cleanup.select
class PhotoGallery(core.models.Image):  # type: ignore[name-defined, misc]
    """
    PhotoGallery Model for Item

    image: second-needed image for gallery
    item: FK to Item that uses this image
    """

    item: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        'Item', on_delete=models.CASCADE, blank=True
    )

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'


class ItemManager(models.Manager):  # type: ignore[type-arg]
    def __init__(self) -> None:
        super(ItemManager, self).__init__()

    def published(self, **kwargs: Any) -> Union[QuerySet[Any], Any]:
        prefetch = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
            to_attr='tags',
        )
        return (
            self.get_queryset()
            .filter(**kwargs)
            .select_related('category')
            .prefetch_related(prefetch)
            .values(
                'name', 'text', 'id', 'category__name', 'image', 'tags__name'
            )
        )

    def item_detail(self, item_id: int) -> Union[QuerySet[Any], Any]:
        prefetch = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        return (
            self.get_queryset()
            .filter(id=item_id)
            .select_related('category')
            .prefetch_related(prefetch)
            .values(
                'name', 'text', 'category__name', 'image', 'tags__name', 'id'
            )
        )


@cleanup.select
class Item(
    core.models.Base, core.models.Image  # type: ignore[name-defined, misc]
):
    """
    Item database object

    is_published: Bool = True. Explains that post/item was published
    name: char[150]. Explains name of this post/item
    text: string. Explains item description.
        Must contain one from words: 'превосходно' or 'роскошно'.
    category: FK to Category. Explains item category
        like kitchen instrument or something else.
    image: ImageFile. Main Item picture that user firstly see in catalog
    is_on_main: Bool = False. Makes item visible on Main page.
    """

    objects = ItemManager()

    text: Union[str, 'RichTextField[Any, Any]'] = RichTextField(
        verbose_name='описание',
        help_text='Опишите объект',
        validators=[
            core.validators.ValidateMustContain('превосходно', 'роскошно'),
        ],
    )

    category: Union[
        Category, 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
        'Category',
        verbose_name='категория',
        help_text='Выберите категорию',
        on_delete=models.SET_NULL,
        null=True,
    )

    tags: Union[
        Tag, 'models.ManyToManyField[Any, Any]'
    ] = models.ManyToManyField(
        'Tag',
        verbose_name='тэги',
    )

    is_on_main: Union[
        bool, 'models.BooleanField[Any, Any]'
    ] = models.BooleanField(
        verbose_name='показать на главной',
        help_text='показывать товар на главной странице?',
        default=False,
    )

    def get_sub_text_words(self, cnt: int = 10) -> str:
        words = self.text.split(maxsplit=cnt)[:-1]
        return ' '.join(words)

    def get_comma_separated_tags(self) -> str:
        tags = (tag.name for tag in self.tags.all())
        return ', '.join(tags)

    class Meta:
        ordering = ('name', 'pk')
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.name[:15])
