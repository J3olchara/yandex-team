from  typing import Any
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

import catalog.models
from . import models


def delete_evaluation(request, user_id: int, item_id: int):
    item: Any = catalog.models.Item.objects.get(pk=item_id)
    user: Any = User.objects.get(pk=user_id)
    evaluation: Any = models.Evaluation.objects.get(user=user, item=item)
    evaluation.delete()
    return redirect(reverse('catalog:int_item_detail', item_id))
