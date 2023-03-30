from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic

from authorisation.models import UserProxy  # noqa: I100
from users import forms  # noqa: I100


class UserList(generic.ListView):  # type: ignore[type-arg]
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    queryset = UserProxy.objects.all()


class UserDetail(generic.DetailView):  # type: ignore[type-arg]
    template_name = 'users/user_detail.html'
    context_object_name = 'current_user'
    queryset = UserProxy.objects


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
