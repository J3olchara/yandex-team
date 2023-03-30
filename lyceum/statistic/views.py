from typing import Any, Dict

from django.db.models import Avg
from django.views import generic

import authorisation.models  # noqa: I100
import rating.models  # noqa: I100


class UsersStatistics(generic.ListView):
    template_name = 'statistic/users_statistics.html'
    queryset = authorisation.models.UserProxy.objects.all()
    context_object_name = 'users'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(UsersStatistics, self).get_context_data(**kwargs)


class ItemStatistic(generic.TemplateView):
    template_name = 'statistic/item_statistic.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        evaluations = rating.models.Evaluation.objects.all()
        count = evaluations.count()
        avg = evaluations.aggregate(Avg('value'))['value__avg']
        if not avg:
            avg = 0
        count = evaluations.count()
        max_evaluation_user = None
        max_evaluation = evaluations.order_by(
            'value', 'change_datetime'
        ).first()
        if max_evaluation:
            max_evaluation_user = max_evaluation.user
        min_evaluation = evaluations.order_by(
            '-value', 'change_datetime'
        ).first()
        min_evaluation_user = None
        if min_evaluation:
            min_evaluation_user = min_evaluation.user

        context['avg'] = avg
        context['count'] = count
        context['max_user'] = max_evaluation_user
        context['min_user'] = min_evaluation_user

        return context
