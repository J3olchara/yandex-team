from django import template
from django.utils.translation import gettext

register = template.Library()


@register.simple_tag()
def translate(string: str) -> str:
    return gettext(string)
