from typing import Any, Dict

from django.views import generic

# isort: off
import authorisation.models  # noqa: I100

# isort: on


class UsersStatistics(generic.ListView):
    template_name = 'statistic/users_statistics.html'
    queryset = authorisation.models.UserProxy.objects.all()
    context_object_name = 'users'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(UsersStatistics, self).get_context_data(**kwargs)
        return context
