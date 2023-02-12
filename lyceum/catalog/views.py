"""CATALOG app pages views"""
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse


def item_list(request: WSGIRequest) -> HttpResponse:
    return HttpResponse('<body>Catalog item list</body>', request)


def item_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    return HttpResponse(f'<body>Item {pk} detail</body>', request)
