"""CATALOG app pages views"""
from typing import Any, List

import catalog.models
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
from django.template.response import TemplateResponse

from . import models


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    template = 'catalog/catalog.html'
    items: Any = models.Item.objects.published(
        order_by=('category__name', 'id'), is_published=True
    )
    data = {
        'items_raw': items,
    }
    response = TemplateResponse(request, template, data)
    return response


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    template = 'catalog/item_page.html'
    item: Any = models.Item.objects.item_detail(item_id)
    images: List[models.PhotoGallery] = models.PhotoGallery.objects.filter(
        item=item_id
    )
    data = {
        'item_raw': item,
        'images': images,
    }
    response = TemplateResponse(request, template, data)
    return response


def regular_item(request: WSGIRequest, item_id: str) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    return item_detail(request, int(item_id))


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got"""
    return item_detail(request, item_id)


def news(request: WSGIRequest) -> HttpResponse:
    """returns page with random 5 new items"""
    template = 'catalog/interesting.html'
    items = catalog.models.Item.objects.random_news()
    data = {'items_raw': items}
    response = TemplateResponse(request, template, data)
    return response


def friday(request: WSGIRequest) -> HttpResponse:
    template = 'catalog/interesting.html'
    items = catalog.models.Item.objects.get_friday()
    data = {'items_raw': items}
    response = TemplateResponse(request, template, data)
    return response


def unchecked(request: WSGIRequest) -> HttpResponse:
    template = 'catalog/interesting.html'
    items = catalog.models.Item.objects.get_unchecked()
    data = {'items_raw': items}
    response = TemplateResponse(request, template, data)
    return response
