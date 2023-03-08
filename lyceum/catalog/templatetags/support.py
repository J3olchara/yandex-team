from typing import Any, Collection, List, Union

from django import template
from django.db.models import QuerySet
from sorl.thumbnail import get_thumbnail

# isort: off
import core  # noqa: I100

# isort: on

register = template.Library()


@register.simple_tag()
def get_image_px(
    image: core.models.Image, px: str, crop: str, quality: int
) -> str:
    return str(image.get_image_px(px=px, crop=crop, quality=quality).url)


@register.simple_tag()
def comma_separated(names: List[str]) -> str:
    return ', '.join(names)


@register.filter()
def group(value: QuerySet[Any], data: str, is_many: Any = True) -> Any:
    dataset = data.split(',')
    if len(dataset) == 3:
        field_name, pk, is_many = dataset
    else:
        field_name, pk = dataset
    qs = value
    j = 0
    i = 0
    grouped = []
    if qs.count():
        grouped.append(qs[0])
        grouped[j][field_name] = [
            grouped[j][field_name],
        ]
        while i < qs.count() - 1:
            if qs[i][pk] != qs[i + 1][pk]:
                grouped.append(qs[i + 1])
                grouped[j][field_name] = [
                    qs[i + 1][field_name],
                ]
                j += 1
            else:
                grouped[j - 1][field_name].append(qs[i + 1][field_name])
            i += 1
    if not is_many:
        return grouped[0]
    return grouped


@register.filter()
def get_words_slice(value: str, words_count: str) -> str:
    words = value.split(maxsplit=int(words_count))
    return ' '.join(words[:-1])


@register.simple_tag()
def get_image_px_by_url(image: str, px: str, crop: str, quality: int) -> str:
    res = str(get_thumbnail(image, px, crop=crop, quality=quality).url)
    return res


@register.simple_tag()
def count(iterable_or_int: Union[Collection[Any], int]) -> List[int]:
    if isinstance(iterable_or_int, Collection):
        iterable_or_int = len(iterable_or_int)
    return list(range(iterable_or_int))
