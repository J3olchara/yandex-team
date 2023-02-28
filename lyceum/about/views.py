"""ABOUT app html views"""
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, render


def description(request: WSGIRequest) -> HttpResponse:
    """returns project description page"""
    response: HttpResponse = render(request, 'about/about_us.html')
    return response
