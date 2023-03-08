"""HOMEPAGE app pages views"""
from typing import List

from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import HttpResponse, render

# isort: off
import catalog  # noqa: I100

# isort: on


def home(request: WSGIRequest) -> HttpResponse:
    """returns homepage"""
    template = 'homepage/index.html'
    items: List[  # type: ignore[name-defined]
        catalog.models.Item
    ] = catalog.models.Item.objects.published(  # type: ignore[attr-defined]
        is_published=True, is_on_main=True
    )
    data = {
        'items': items,
    }
    response: HttpResponse = render(request, template, data)
    return response


def coffee(request: WSGIRequest) -> HttpResponse:
    """returns error page that django cant generate because he is a tea pot"""
    response: HttpResponse = render(request, 'homepage/teapot.html')
    response.status_code = 418
    return response


def test(request: WSGIRequest) -> HttpResponse:
    """testing a reversion russian words"""
    if request.GET:
        if request.GET.get('test'):
            return render(
                request,
                'homepage/test.html',
                {'test': request.GET.get('test')},
            )
    raise Http404()
