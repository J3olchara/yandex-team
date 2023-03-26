from typing import Any, Optional

import django.contrib.auth.forms as default_forms
import django.contrib.auth.models as default_models
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from . import models


class LoginForm(default_forms.AuthenticationForm):
    remember_me = forms.BooleanField(
        label=_('Запомнить меня'),
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mb-4',
            }
        ),
        required=False,
    )

    def __init__(self, *args: Any, **kwargs: Any):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'placeholder': _('Username'),
            }
        )
        self.fields['password'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder': _('Password'),
                'type': 'password',
            }
        )


class PasswordChangeForm(default_forms.PasswordChangeForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'password',
            }
        )
        self.fields['old_password'].widget = widget
        self.fields['new_password1'].widget = widget
        self.fields['new_password2'].widget = widget


class PasswordResetForm(default_forms.PasswordResetForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'email',
            }
        )


class PasswordResetConfirmForm(default_forms.SetPasswordForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)
        widget = forms.PasswordInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'password',
            }
        )
        self.fields['new_password1'].widget = widget
        self.fields['new_password2'].widget = widget


class SignUpForm(default_forms.UserCreationForm):  # type: ignore[type-arg]
    email = forms.EmailField(
        label=_('Ваш email'),
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'type': 'email',
            }
        ),
    )

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def clean_email(self) -> Optional[str]:
        email = self.cleaned_data.get('email')
        if default_models.User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Этот email уже используется'))
        return email

    def save(self, commit: bool = True) -> models.ActivationToken:
        instance = super(SignUpForm, self).save(commit=commit)
        instance.is_active = settings.NEW_USERS_ACTIVATED
        token = models.ActivationToken.objects.create(
            user=instance,
        )
        instance.save()
        return token

    class Meta:
        model = models.UserProxy
        fields = ['email', 'username', 'password1', 'password2']
