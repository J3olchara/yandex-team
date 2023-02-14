"""HOMEPAGE app pages views"""
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404
from django.shortcuts import HttpResponse, render


def home(request: WSGIRequest) -> HttpResponse:
    """returns homepage"""
    response: HttpResponse = render(request, r'homepage/index.html')
    return response


def coffee(request: WSGIRequest) -> HttpResponse:
    """returns error page that django cant generate because he is a tea pot"""
    response: HttpResponse = render(request, r'homepage/teapot.html')
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
