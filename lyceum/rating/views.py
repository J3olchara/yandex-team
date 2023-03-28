from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View

# isort: off
from . import models  # noqa: I100
import catalog.models  # noqa: I100

# isort: on


class DeleteEvaluation(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL

    def get(self, request: HttpRequest, item_id: int) -> HttpResponse:
        item: Any = get_object_or_404(catalog.models.Item, pk=item_id)
        evaluation = models.Evaluation.objects.filter(
            user=request.user, item=item
        ).first()
        if evaluation:
            evaluation.delete()
        return redirect(
            reverse_lazy(
                'catalog:int_item_detail', kwargs={'item_id': item_id}
            )
        )
