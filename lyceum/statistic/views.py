from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.aggregates import Avg
from django.views import generic

import authorisation.models
import rating.models


class UsersStatistics(generic.ListView):
    template_name = 'statistic/users_statistics.html'
    context_object_name = 'users'
    queryset = authorisation.models.UserProxy.objects.with_evaluations()


class ItemStatistic(generic.TemplateView):
    template_name = 'statistic/item_statistic.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        evaluations = rating.models.Evaluation.objects.all()
        avg = evaluations.aggregate(Avg('value'))['value__avg']
        if not avg:
            avg = 0
        count = evaluations.count()
        max_evaluation_user = None
        max_evaluation = evaluations.order_by('value', 'changed').first()
        if max_evaluation:
            max_evaluation_user = max_evaluation.user
        min_evaluation = evaluations.order_by('-value', 'changed').first()
        min_evaluation_user = None
        if min_evaluation:
            min_evaluation_user = min_evaluation.user

        context['avg'] = avg
        context['count'] = count
        context['max_user'] = max_evaluation_user
        context['min_user'] = min_evaluation_user

        return context


class RatedStatistic(LoginRequiredMixin, generic.ListView):
    template_name = 'statistic/rated_statistic.html'
    context_object_name = 'rated_items'

    def get_queryset(self):
        return (
            rating.models.Evaluation.objects.filter(user__id=self.request.user.id)
        )
