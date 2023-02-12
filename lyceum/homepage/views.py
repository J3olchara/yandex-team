from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse


def home(request: WSGIRequest) -> HttpResponse:
    return HttpResponse('<body>Home page</body>')
