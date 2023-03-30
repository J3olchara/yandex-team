from typing import Any, Collection, Iterable, List, Optional, Union

from django import template
from django.db.models import Avg
from sorl.thumbnail import get_thumbnail

import core.models

register = template.Library()


@register.simple_tag()
def get_image_px(
    image: core.models.Image,  # type: ignore[name-defined]
    px: str,
    crop: str,
    quality: int,
) -> str:
    return str(image.get_image_px(px=px, crop=crop, quality=quality).url)


@register.filter()
def get_avg_evaluation(user):
    avg = user.evaluations.aggregate(avg_evaluations=Avg('value'))[
        'avg_evaluations'
    ]
    if avg is not None:
        return avg
    return 0


@register.filter()
def get_worth_evaluation(user):
    if user.evaluations.count():
        print(user)
        return user.evaluations.last()
    return 0


@register.filter()
def get_best_evaluation(value, **kwargs):
    if value.evaluations.count():
        print(value)
        return value.evaluations.first()
    return 0


@register.simple_tag()
def comma_separated(names: List[str]) -> str:
    return ', '.join(names)


@register.filter()
def group_items(
    value: Any, data: str, is_one: bool = False
) -> Union[List[Any], Any]:
    data_set = data.split(',')
    field_name, pk = data_set[:2]
    if len(data_set) == 3:
        is_one = data_set[2].lower() in ['1', 'y', 'true', 'yes']
    jindex = 0
    index = 0
    grouped: List[Any] = []
    if value:
        grouped.append(value[0])
        grouped[jindex][field_name] = [
            grouped[jindex][field_name],
        ]
        jindex += 1
        while index < value.count() - 1:
            if value[index][pk] != value[index + 1][pk]:
                grouped.append(value[index + 1])
                grouped[jindex][field_name] = [
                    value[index + 1][field_name],
                ]
                jindex += 1
            else:
                grouped[jindex - 1][field_name].append(
                    value[index + 1][field_name]
                )
            index += 1
    if is_one:
        return grouped[0]
    return grouped


@register.filter()
def make_unique(iterable: Iterable[Any]) -> Iterable[Any]:
    return list({v['id']: v for v in iterable}.values())[:5]


@register.filter()
def get_words_slice(value: str, words_count: str) -> str:
    words = value.split(maxsplit=int(words_count))
    return ' '.join(words[:-1])


@register.simple_tag()
def get_image_px_by_url(
    image: str, px: str, crop: str, quality: int
) -> Optional[str]:
    if image:
        return str(get_thumbnail(image, px, crop=crop, quality=quality).url)
    return 'NaN'


@register.simple_tag()
def count(iterable_or_int: Union[Collection[Any], int]) -> List[int]:
    if isinstance(iterable_or_int, Collection):
        iterable_or_int = len(iterable_or_int)
    return list(range(iterable_or_int))
