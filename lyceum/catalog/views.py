"""CATALOG app pages views"""
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    response: HttpResponse = render(request, 'catalog/catalog.html')
    return response


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    response: HttpResponse = render(
        request,
        'catalog/item_page.html',
        {
            'item_id': item_id,
        },
    )
    return response


def regular_item(request: WSGIRequest, item_id: str) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    response: HttpResponse = render(
        request,
        'catalog/item_page.html',
        {
            'item_id': item_id,
        },
    )
    return response


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got"""
    response: HttpResponse = render(
        request,
        'catalog/item_page.html',
        {
            'item_id': item_id,
        },
    )
    return response
