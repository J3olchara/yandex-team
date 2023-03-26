"""HOMEPAGE app pages views"""

from django.core.handlers.wsgi import WSGIRequest
from django.db.models.query import QuerySet
from django.http import Http404
from django.shortcuts import HttpResponse, render
from django.template.response import TemplateResponse

# isort: off
import catalog  # noqa: I100

# isort: on


def home(request: WSGIRequest) -> HttpResponse:
    """returns homepage"""
    template = 'homepage/index.html'
    items: QuerySet[  # type: ignore[name-defined]
        catalog.models.Item
    ] = catalog.models.Item.objects.published(  # type: ignore[attr-defined]
        order_by=('name', 'id'), is_published=True, is_on_main=True
    )
    data = {
        'items_raw': items,
    }
    return TemplateResponse(request, template, data)


def coffee(request: WSGIRequest) -> HttpResponse:
    """returns error page that django cant generate because he is a tea pot"""
    response: HttpResponse = TemplateResponse(request, 'homepage/teapot.html')
    response.status_code = 418
    if request.user.is_authenticated:
        request.user.profile.coffee_break()
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
