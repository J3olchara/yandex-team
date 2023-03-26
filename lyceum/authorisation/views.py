from typing import Any, Dict

import django.contrib.auth.views as default_views
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

from . import forms, models


class CustomLoginView(default_views.LoginView):
    form_class = forms.LoginForm
    template_name = 'authorisation/login.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form: Any) -> HttpResponse:
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class CustomChangePasswordDone(default_views.PasswordChangeDoneView):
    template_name = 'authorisation/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CustomChangePasswordDone, self).get_context_data(
            **kwargs
        )
        context['alerts'] = [
            {'type': 'success', 'text': _('Пароль успешно изменён')}
        ]
        return context


class CustomPasswordResetDone(default_views.PasswordResetDoneView):
    template_name = 'authorisation/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CustomPasswordResetDone, self).get_context_data(
            **kwargs
        )
        head = _('Письмо с инструкциями по восстановлению пароля отправлено')
        p1 = _(
            'Мы отправили вам инструкцию по установке нового '
            'пароля на указанный адрес электронной почты'
            '(если в нашей базе данных есть такой адрес). '
            'Вы должны получить ее в ближайшее время.'
        )
        p2 = _(
            'Если вы не получили письмо, пожалуйста, убедитесь, что '
            'вы ввели адрес с которым Вы зарегистрировались,'
            ' и проверьте папку со спамом.'
        )
        context['message'] = (
            f'<h1>{head}</h1>\n' f'<p>{p1}</p>\n' f'<p>{p2}</p>'
        )
        return context


class CustomPasswordResetComplete(default_views.PasswordResetCompleteView):
    template_name = 'authorisation/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CustomPasswordResetComplete, self).get_context_data(
            **kwargs
        )
        context['alerts'] = [
            {'type': 'success', 'text': _('Пароль успешно изменён')}
        ]
        return context


def signup(request: WSGIRequest) -> HttpResponse:
    template = 'authorisation/signup.html'
    form = forms.SignUpForm(request.POST or None)
    if form.is_valid():
        token = form.save()
        url = token.get_url(f'http://{get_current_site(request)}')
        username = form.data['username']
        message = (
            _(
                f'Благодарим за регистрацию на нашем сайте!\n\n'
                f'Ваш логин: {username}\n'
                f'Для активации аккаунта перейдите по ссылке\n'
            )
            + url
        )
        mail.send_mail(
            subject=str(_('Активация аккаунта')),
            message=message,
            from_email=settings.SITE_EMAIL,
            recipient_list=[form.data['email']],
        )
        return redirect(reverse('authorisation:signup_done'))
    return TemplateResponse(request, template, {'form': form})


def signup_confirm(
    request: WSGIRequest, user_id: int, token: models.ActivationToken
) -> HttpResponse:
    template = 'authorisation/done.html'
    token = get_object_or_404(
        models.ActivationToken.objects,
        user=user_id,
        token=token,
    )
    data = {}
    if not token.expired():
        token.user.is_active = True
        token.user.save()
        token.delete()
        data['alerts'] = [
            {'type': 'success', 'text': _('Ваш аккаунт успешно активирован!')}
        ]
    else:
        data['alerts'] = [
            {
                'type': 'danger',
                'text': _(
                    'Ссылка на активацию аккаунта истекла. '
                    'Обратитесь к администрации'
                ),
            }
        ]
    return TemplateResponse(request, template, data)


def signup_done(request: WSGIRequest) -> HttpResponse:
    template = 'authorisation/done.html'
    alerts = [
        {
            'type': 'success',
            'text': _(
                'На вашу электронную отправлена ссылка на активацию аккаунта.'
            ),
        }
    ]
    return TemplateResponse(request, template, {'alerts': alerts})
