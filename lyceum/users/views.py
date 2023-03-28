from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

# isort: off
from . import forms  # noqa: I100
from authorisation.models import UserProxy  # noqa: I100

# isort: on


class UserList(generic.ListView):  # type: ignore[type-arg]
    template_name = 'users/user_list.html'
    queryset = UserProxy.objects.all()
    context_object_name = 'users'


class UserDetail(generic.DetailView):  # type: ignore[type-arg]
    template_name = 'users/user_detail.html'

    def get_queryset(self) -> Any:
        return get_object_or_404(UserProxy.objects, id=self.kwargs['user_id'])


class Profile(LoginRequiredMixin, generic.FormView):  # type: ignore[type-arg]
    template_name = 'users/profile.html'
    form_class = forms.EditProfile
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = {
            'data': {
                **model_to_dict(self.request.user),  # type: ignore[arg-type]
                **model_to_dict(
                    self.request.user.profile  # type: ignore[union-attr]
                ),
                **dict(self.request.POST.items()),
            }
            or None,
            'files': self.request.FILES or None,
        }
        return kwargs

    def form_valid(self, form: forms.EditProfile) -> HttpResponse:
        form.save(user=self.request.user)
        return super(Profile, self).form_valid(form)
