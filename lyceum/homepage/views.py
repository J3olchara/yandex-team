"""HOMEPAGE app pages views"""
from typing import Any, Dict

from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpRequest
from django.shortcuts import HttpResponse, render
from django.template.response import TemplateResponse
from django.views import generic

# isort: off
import catalog.models  # noqa: I100

# isort: on


class Home(generic.ListView):
    """returns homepage"""
    template_name = 'homepage/index.html'
    queryset = catalog.models.Item.objects.published(  # type: ignore[attr-defined]
        order_by=('name', 'id'), is_published=True, is_on_main=True
    )
    context_object_name = 'items_raw'


class Coffee(generic.TemplateView):
    """returns error page that django cant generate because he is a tea pot"""
    template_name = 'homepage/teapot.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        response = super(Coffee, self).get(request, *args, **kwargs)
        response.status_code = 418
        if request.user.is_authenticated:
            request.user.profile.coffee_break()
        return response


class Test(generic.TemplateView):
    """empty page for testing information"""
    template_name = 'homepage/test.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(Test, self).get_context_data(**kwargs)
        context['test'] = self.request.GET().get('test')
        return context
