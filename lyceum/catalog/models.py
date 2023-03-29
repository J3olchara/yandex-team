"""
Database models from Catalog app

There is models that helping users to get information from catalog
like items descriptions, items, their tags, categories and other
"""
from datetime import datetime, timedelta
from typing import Any, Iterable, Optional, Set, Union

from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.db.models import F, QuerySet
from django.db.models.aggregates import Count
from django_cleanup import cleanup
from pytz import timezone

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

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        self.save()


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

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        self.save()


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


class ItemManager(models.Manager['Item']):
    def published(
        self, order_by: Optional[Iterable[str]] = None, **kwargs: Any
    ) -> Union[QuerySet[Any], Any]:
        if order_by is None:
            order_by = []
        prefetch = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        return (
            self.get_queryset()
            .filter(**kwargs)
            .select_related('category')
            .prefetch_related(prefetch)
            .order_by(*order_by)
            .values(
                'name', 'text', 'id', 'category__name', 'image', 'tags__name'
            )
        )

    def item_detail(self, item_id: int) -> Union[QuerySet[Any], Any]:
        prefetch_tags = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        prefetch_images = models.Prefetch(
            'PhotoGallery', queryset=PhotoGallery.objects.all().only('image')
        )
        return (
            self.get_queryset()
            .filter(id=item_id)
            .select_related('category')
            .prefetch_related(prefetch_tags)
            .prefetch_related(prefetch_images)
            .values(
                'name', 'text', 'category__name', 'image', 'tags__name', 'id'
            )
        )

    def random_news(self) -> Union[QuerySet[Any], Any]:
        prefetch_tags = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        now = datetime.now(tz=timezone(settings.TIME_ZONE))
        count = self.filter(
            creation_date__range=(now - timedelta(days=7), now)
        ).aggregate(count=Count('id'))['count']
        rand: Set[int] = set()
        while len(rand) < 5 and len(rand) < count:
            qs = (
                self.get_queryset()
                .filter(creation_date__range=(now - timedelta(days=7), now))
                .order_by('?')
                .values('id')[:5]
            )
            for item in qs:
                if len(rand) < 5:
                    rand.add(item['id'])
        return (
            self.get_queryset()
            .filter(
                creation_date__range=(now - timedelta(days=7), now),
                id__in=rand,
            )
            .prefetch_related(prefetch_tags)
            .values(
                'name', 'text', 'id', 'category__name', 'image', 'tags__name'
            )
        )

    def get_friday(self) -> Union[QuerySet[Any], Any]:
        prefetch_tags = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        return (
            self.get_queryset()
            .filter(last_edit_date__iso_week_day=5)
            .prefetch_related(prefetch_tags)
            .order_by('-last_edit_date')[:5]
            .values(
                'name', 'text', 'id', 'category__name', 'image', 'tags__name'
            )
        )

    def get_unchecked(self) -> Union[QuerySet[Any], Any]:
        prefetch_tags = models.Prefetch(
            'tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        return (
            self.get_queryset()
            .filter(
                last_edit_date__date=F('last_edit_date'),
                last_edit_date__hour=F('last_edit_date'),
                last_edit_date__minute=F('last_edit_date'),
            )
            .prefetch_related(prefetch_tags)
            .values(
                'name', 'text', 'id', 'category__name', 'image', 'tags__name'
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
        related_name='category',
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

    last_edit_date = models.DateTimeField(
        verbose_name='Дата последнего изменения',
        auto_now=True,
    )

    creation_date = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('name', 'pk')
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self) -> str:
        return str(self.id) + ' ' + str(self.name[:15])
