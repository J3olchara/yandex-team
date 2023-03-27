"""CATALOG app pages views"""
from typing import Any

from catalog import models
from catalog.models import Item as Catalog_Item
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Avg
from django.shortcuts import HttpResponse, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# isort: off
import rating.forms  # noqa: I100
import rating.models  # noqa: I100

# isort: on


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


class ItemDetailView(TemplateView):
    template_name = 'catalog/item_page.html'
    model = Catalog_Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('item_id')
        item = Catalog_Item.objects.item_detail(item_id)
        item_object: Any = get_object_or_404(Catalog_Item, pk=item_id)
        images = models.PhotoGallery.objects.filter(item=item_id)
        item_evalution = rating.models.Evaluation.objects.filter(
            item=item_object
        )
        avg = item_evalution.aggregate(Avg('value'))['value__avg']
        context['average'] = 0
        if avg:
            context['average'] = round(avg, 5)
        context['item_raw'] = item
        context['images'] = images
        context['count'] = item_evalution.count()
        evaluation = rating.models.Evaluation.objects.filter(
            user=self.request.user.id, item=item_object
        ).first()
        form = rating.forms.EvaluationForm(
            self.request.POST or None, instance=evaluation
        )
        context['evaluation_form'] = form
        return context

    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(self.model, id=item_id)
        form = rating.forms.EvaluationForm(request.POST or None)

        if form.is_valid():
            value = form.cleaned_data.get('value')
            rating.models.Evaluation.objects.update_or_create(
                user=request.user, item=item, defaults={'value': value}
            )
            return redirect(
                reverse_lazy(
                    'catalog:int_item_detail', kwargs={'item_id': item_id}
                )
            )

        return self.render_to_response(self.get_context_data(form=form))


def regular_item(request: WSGIRequest, item_id: str) -> HttpResponse:
    """returns item $item_id description that was got from regexp"""
    return ItemDetailView.as_view()(request, item_id=int(item_id))


def converter_item(request: WSGIRequest, item_id: int) -> HttpResponse:
    """returns item $item_id description that was got"""
    return ItemDetailView.as_view()(request, item_id=item_id)


def news(request: WSGIRequest) -> HttpResponse:
    """returns page with random 5 new items"""
    template = 'catalog/interesting.html'
    items = models.Item.objects.random_news()
    data = {'items_raw': items}
    return TemplateResponse(request, template, data)


def friday(request: WSGIRequest) -> HttpResponse:
    template = 'catalog/interesting.html'
    items = models.Item.objects.get_friday()
    data = {'items_raw': items}
    return TemplateResponse(request, template, data)


def unchecked(request: WSGIRequest) -> HttpResponse:
    template = 'catalog/interesting.html'
    items = models.Item.objects.get_unchecked()
    data = {'items_raw': items}
    return TemplateResponse(request, template, data)
