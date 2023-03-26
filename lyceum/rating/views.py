from typing import Any
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from lyceum.settings import LOGIN_URL
from django.urls import reverse

import catalog.models
from . import models


@login_required(login_url=LOGIN_URL)
def delete_evaluation(request, item_id: int):
    item: Any = catalog.models.Item.objects.get(pk=item_id)
    evaluation: Any = get_object_or_404(
        models.Evaluation, user=request.user.id, item=item
    )
    evaluation.delete()
    return redirect(reverse('catalog:int_item_detail', item_id))
