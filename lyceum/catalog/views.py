"""CATALOG app pages views"""
from typing import Any, List

import catalog.models
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse
from django.template.response import TemplateResponse

from . import models

"""CATALOG app pages views"""
from typing import Any, List, Dict

import catalog.models
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, reverse
from django.template.response import TemplateResponse
from django.views import generic

from . import models


class ItemList(generic.ListView):
    template_name = 'catalog/catalog.html'
    model = models.Item
    queryset = models.Item.objects.published(
        order_by=('category__name', 'id'), is_published=True
    )
    context_object_name = 'items_raw'


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    template = 'catalog/item_page.html'
    item: Any = models.Item.objects.item_detail(item_id)
    images: List[models.PhotoGallery] = models.PhotoGallery.objects.filter(
        item=item_id
    )
    data = {
        'item_raw': item,
        'images': images,
    }
    return TemplateResponse(request, template, data)


class RegularItem(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any):
        return reverse('catalog:int_item_detail', kwargs={'item_id': self.kwargs['item_id']})


class ConverterItem(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any):
        return reverse('catalog:int_item_detail', kwargs={'item_id': self.kwargs['item_id']})


class News(generic.ListView):
    template_name = 'catalog/interesting.html'
    context_object_name = 'items_raw'

    def get_queryset(self):
        return catalog.models.Item.objects.random_news()


class Friday(generic.ListView):
    template_name = 'catalog/interesting.html'
    queryset = catalog.models.Item.objects.get_friday()
    context_object_name = 'items_raw'


class Unchecked(generic.ListView):
    template_name = 'catalog/interesting.html'
    queryset = catalog.models.Item.objects.get_unchecked()
    context_object_name = 'items_raw'
