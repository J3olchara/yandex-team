"""CATALOG app pages views"""
from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, get_object_or_404, render

from . import models


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    template = 'catalog/catalog.html'
    items: List[models.Item] = models.Item.objects.published(
        is_published=True
    ).order_by('category', 'pk')
    data = {
        'items': items,
    }
    response: HttpResponse = render(request, template, data)
    return response


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    template = 'catalog/item_page.html'
    item: models.Item = get_object_or_404(
        models.Item.objects.published(),
        id=item_id,
    )
    images: List[models.PhotoGallery] = models.PhotoGallery.objects.filter(
        item=item
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
