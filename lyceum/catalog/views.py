"""CATALOG app pages views"""
from typing import Any, List

import catalog.models
import rating.models
import rating.forms
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import HttpResponse, redirect
from django.template.response import TemplateResponse
from django.urls import reverse

from . import models


def item_list(request: WSGIRequest) -> HttpResponse:
    """returns item list page"""
    template = 'catalog/catalog.html'
    items: Any = models.Item.objects.published(
        order_by=('category__name', 'id'), is_published=True
    )
    data = {
        'items_raw': items,
    }
    return TemplateResponse(request, template, data)


def item_detail(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description"""
    template = 'catalog/item_page.html'
    item: Any = models.Item.objects.item_detail(item_id)
    item_object: Any = models.Item.objects.get(id=item_id)
    images: List[models.PhotoGallery] = models.PhotoGallery.objects.filter(
        item=item_id
    )
    data = {
        'item_raw': item,
        'images': images,
    }
    if request.user.is_authenticated:
        evaluation: Any = rating.models.Evaluation.objects.filter(user=request.user.id, item=item_object).first()
        if evaluation:
            data['url_to_delete'] = reverse('rating:delete_evaluation', item_id, request.user.id)
        form: Any = rating.forms.EvaluationForm(request.POST or None, instance=evaluation)
        if request.POST and form.is_valid():
            if evaluation:
                form.save()
            else:
                value = form.cleaned_data.get('value')
                rating.models.Evaluation.objects.create(user=request.user, item=item_object, value=value)
            return redirect(reverse('catalog:catalog', item_id))
        data['evaluation_form'] = form
    return TemplateResponse(request, template, data)


def regular_item(request: WSGIRequest, item_id: str) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    return item_detail(request, int(item_id))


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got"""
    return item_detail(request, item_id)


def news(request: WSGIRequest) -> HttpResponse:
    """returns page with random 5 new items"""
    template = 'catalog/interesting.html'
    items = catalog.models.Item.objects.random_news()
    data = {'items_raw': items}
    return TemplateResponse(request, template, data)


def friday(request: WSGIRequest) -> HttpResponse:
    template = 'catalog/interesting.html'
    items = catalog.models.Item.objects.get_friday()
    data = {'items_raw': items}
    return TemplateResponse(request, template, data)


def unchecked(request: WSGIRequest) -> HttpResponse:
    template = 'catalog/interesting.html'
    items = catalog.models.Item.objects.get_unchecked()
    data = {'items_raw': items}
    return TemplateResponse(request, template, data)
