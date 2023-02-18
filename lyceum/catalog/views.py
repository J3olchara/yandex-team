"""CATALOG app pages views"""
import re

from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import HttpResponse, render


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    response: HttpResponse = render(request, r'catalog/catalog.html')
    return response


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    response: HttpResponse = render(
        request,
        r'catalog/item_page.html',
        {
            'item_id': item_id,
        },
    )
    return response


def regular_item(request: WSGIRequest) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    pattern: str = r'.*/re/([1-9]\d*)/'
    regexp = re.search(pattern, request.path)
    if regexp:
        item_id: int = int(regexp.group(1))
        response: HttpResponse = render(
            request,
            r'catalog/item_page.html',
            {
                'item_id': item_id,
            },
        )
        return response
    raise Http404()


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got"""
    response: HttpResponse = render(
        request,
        r'catalog/item_page.html',
        {
            'item_id': item_id,
        },
    )
    return response
