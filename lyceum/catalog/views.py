"""CATALOG app pages views"""
import re

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import Http404, HttpResponse, render


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    response: HttpResponse = render(request, r'catalog/catalog.html')
    return response


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    response: HttpResponse = render(request, r'catalog/item_page.html', {
        'item_id': item_id
    })
    return response


def regular_item(request: WSGIRequest) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    pattern: str = r'.*/re/([1-9]\d*)/'
    if re.match(pattern, request.path):
        item_id: int = int(re.search(pattern, request.path).group(1))
        response: HttpResponse = HttpResponse(
            f'regexp Item {item_id} detail', request
        )
        return response
    raise Http404()


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got by self written converter"""
    response: HttpResponse = HttpResponse(
        f'regexp Item {item_id} detail', request
    )
    return response
