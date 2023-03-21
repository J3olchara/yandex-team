from typing import Any, Dict

from django.utils.translation import gettext_lazy as _
import django.contrib.auth.views as default_views
from django.urls import reverse_lazy
from django.http import HttpResponse

from . import forms


class CustomLoginView(default_views.LoginView):
    form_class = forms.LoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form: Any) -> HttpResponse:
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class CustomChangePasswordDone(default_views.PasswordChangeDoneView):
    template_name = 'users/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CustomChangePasswordDone, self).get_context_data(**kwargs)
        context['alerts'] = [
            {
                'type': 'success',
                'text': _('Пароль успешно изменён')
            }
        ]
        return context


class CustomPasswordResetDone(default_views.PasswordResetDoneView):
    template_name = 'users/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CustomPasswordResetDone, self).get_context_data(**kwargs)
        head = _('Письмо с инструкциями по восстановлению пароля отправлено')
        p1 = _(
            'Мы отправили вам инструкцию по установке нового пароля на указанный адрес электронной почты'
            '(если в нашей базе данных есть такой адрес). Вы должны получить ее в ближайшее время.'
        )
        p2 = _(
            'Если вы не получили письмо, пожалуйста, убедитесь, что вы ввели адрес с которым Вы зарегистрировались,'
            ' и проверьте папку со спамом.'
        )
        context['message'] = (
            f'<h1>{head}</h1>\n'
            f'<p>{p1}</p>\n'
            f'<p>{p2}</p>'
        )
        return context


class CustomPasswordResetComplete(default_views.PasswordResetCompleteView):
    template_name = 'users/done.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(CustomPasswordResetComplete, self).get_context_data(**kwargs)
        context['alerts'] = [
            {
                'type': 'success',
                'text': _('Пароль успешно изменён')
            }
        ]
        return context



