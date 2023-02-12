"""ABOUT app html views"""
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse


def description(request: WSGIRequest) -> HttpResponse:
    """returns project description page"""
    return HttpResponse('<body>About</body>')
