from typing import Any
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from lyceum.settings import LOGIN_URL
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

import catalog.models
from . import models


class Delete_Evaluation(LoginRequiredMixin, View):
    login_url = LOGIN_URL

    def get(self, request, item_id):
        item: Any = get_object_or_404(catalog.models.Item, pk=item_id)
        evaluation = models.Evaluation.objects.filter(user=request.user, item=item).first()
        if evaluation:
            evaluation.delete()
        return redirect(reverse_lazy('catalog:int_item_detail', kwargs={'item_id': item_id}))