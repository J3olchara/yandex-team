from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from . import forms


def user_list(request: WSGIRequest) -> HttpResponse:
    template = 'users/user_list.html'
    data = {'users': User.objects.all().filter(is_active=True)}
    return render(request, template, data)


def user_detail(request: WSGIRequest, user_id: int) -> HttpResponse:
    template = 'users/user_detail.html'
    data = {'current_user': get_object_or_404(User.objects, id=user_id)}
    return render(request, template, data)


@login_required()
def profile(request: WSGIRequest) -> HttpResponse:
    template = 'users/profile.html'
    form_data = {
        **model_to_dict(request.user),  # type: ignore[arg-type]
        **model_to_dict(request.user.profile),  # type: ignore[union-attr]
        **dict(request.POST.items()),
    }
    form = forms.EditProfile(form_data or None, files=request.FILES or None)
    data = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save(user=request.user)
            return redirect(reverse('users:profile'))
    return render(request, template, data)
