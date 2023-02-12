"""CATALOG app pages views"""
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    return HttpResponse('<body>Catalog item list</body>', request)


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    return HttpResponse(f'<body>Item {item_id} detail</body>', request)
