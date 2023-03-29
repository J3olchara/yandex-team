"""HOMEPAGE app pages views"""
from typing import Any, Dict

from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.shortcuts import HttpResponse
from django.views import generic

import catalog  # noqa: I100


class Home(generic.ListView):  # type: ignore[type-arg]
    """returns homepage"""

    template_name = 'homepage/index.html'
    context_object_name = 'items_raw'

    def get_queryset(self) -> QuerySet['catalog.models.Item']:
        return catalog.models.Item.objects.published(
            order_by=('name', 'id'), is_on_main=True
        )


class Coffee(generic.TemplateView):
    """returns error page that django cant generate because he is a tea pot"""

    template_name = 'homepage/teapot.html'

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
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
        context['test'] = self.request.GET.get('test')
        return context
