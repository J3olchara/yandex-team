from typing import Any, Collection, List, Union

from django import template
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
def get_image_px_by_url(
    image: core.models.Image, px: str, crop: str, quality: int
) -> str:
    return str(get_thumbnail(image, px, crop=crop, quality=quality).url)


@register.simple_tag()
def count(iterable_or_int: Union[Collection[Any], int]) -> List[int]:
    if isinstance(iterable_or_int, Collection):
        iterable_or_int = len(iterable_or_int)
    return list(range(iterable_or_int))
