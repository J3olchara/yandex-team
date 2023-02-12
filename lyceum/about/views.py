from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse


def description(request: WSGIRequest) -> HttpResponse:
    return HttpResponse('<body>About</body>')
