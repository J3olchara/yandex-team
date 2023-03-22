from django.shortcuts import render, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from . import forms


def user_list(request: WSGIRequest) -> HttpResponse:
    template = 'users/user_list.html'
    data = {
        'users': User.objects.all().filter(is_active=True)
    }
    return render(request, template, data)


def user_detail(request: WSGIRequest, user_id: int) -> HttpResponse:
    template = 'users/user_detail.html'
    data = {
        'current_user': get_object_or_404(
            User.objects,
            id=user_id
        )
    }
    return render(request, template, data)


@login_required()
def profile(request: WSGIRequest) -> HttpResponse:
    template = 'users/profile.html'
    profile = model_to_dict(request.user.profile)
    user = model_to_dict(request.user)
    form = forms.EditProfile(user or None, profile or None)
    data = {
        'form': form
    }
    if request.method == 'POST' and form.is_valid():
        form.save()
    return render(request, template, data)


