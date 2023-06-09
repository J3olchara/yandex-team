"""CATALOG app pages views"""
from typing import Any, Dict

from django.db.models import Avg
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic

import catalog.models
import rating.forms
import rating.models


class ItemList(generic.ListView):  # type: ignore[type-arg]
    template_name = 'catalog/catalog.html'
    model = catalog.models.Item
    queryset = catalog.models.Item.objects.published(
        order_by=('category__name', 'id')
    )
    context_object_name = 'items_raw'


class ItemDetailView(generic.TemplateView):
    template_name = 'catalog/item_page.html'
    model = catalog.models.Item

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        item_id = self.kwargs.get('item_id')
        item = catalog.models.Item.objects.item_detail(item_id)
        item_object: Any = get_object_or_404(catalog.models.Item, pk=item_id)
        images = catalog.models.PhotoGallery.objects.filter(item=item_id)
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
        context['evaluation'] = evaluation
        return context

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
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


class RegularItem(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        return reverse(
            'catalog:int_item_detail',
            kwargs={'item_id': self.kwargs['item_id']},
        )


class ConverterItem(generic.RedirectView):
    permanent = False

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> str:
        return reverse(
            'catalog:int_item_detail',
            kwargs={'item_id': self.kwargs['item_id']},
        )


class News(generic.ListView):  # type: ignore[type-arg]
    template_name = 'catalog/interesting.html'
    context_object_name = 'items_raw'

    def get_queryset(self) -> QuerySet[catalog.models.Item]:
        return catalog.models.Item.objects.random_news()


class Friday(generic.ListView):  # type: ignore[type-arg]
    template_name = 'catalog/interesting.html'
    queryset = catalog.models.Item.objects.get_friday()
    context_object_name = 'items_raw'


class Unchecked(generic.ListView):  # type: ignore[type-arg]
    template_name = 'catalog/interesting.html'
    queryset = catalog.models.Item.objects.get_unchecked()
    context_object_name = 'items_raw'
