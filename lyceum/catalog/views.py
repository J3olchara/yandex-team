"""CATALOG app pages views"""
from typing import Any, List

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render

from . import models


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    template = 'catalog/catalog.html'
    items: Any = models.Item.objects.published(is_published=True).order_by(
        'category__name', 'id'
    )
    data = {
        'items': items,
    }
    response: HttpResponse = render(request, template, data)
    return response


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    template = 'catalog/item_page.html'
    item: Any = models.Item.objects.item_detail(item_id)
    images: List[models.PhotoGallery] = models.PhotoGallery.objects.filter(
        item=item_id
    )
    data = {
        'item': item,
        'images': images,
    }
    response: HttpResponse = render(request, template, data)
    return response


def regular_item(request: WSGIRequest, item_id: str) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    return item_detail(request, int(item_id))


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got"""
    return item_detail(request, item_id)
