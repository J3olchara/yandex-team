"""HOMEPAGE app pages views"""
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse


def home(request: WSGIRequest) -> HttpResponse:
    """returns homepage"""
    return HttpResponse('<body>Home page</body>', request)
