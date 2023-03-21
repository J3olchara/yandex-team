import django.contrib.auth.forms as default_forms
from django import forms


class LoginForm(default_forms.AuthenticationForm):
    remember_me = forms.BooleanField(
        label='Запомнить меня',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input mb-4',

            }
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'placeholder': 'Username',
            }
        )
        self.fields['password'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-3',
                'placeholder':  'Password',
                'type': 'password'
            }
        )


class PasswordChangeForm(default_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
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
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'email',
            }
        )


class PasswordResetConfirmForm(default_forms.SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetConfirmForm, self).__init__(*args, **kwargs)
        widget = forms.TextInput(
            attrs={
                'class': 'form-control form-control-lg mb-2',
                'type': 'password',
            }
        )
        self.fields['new_password1'].widget = widget
        self.fields['new_password2'].widget = widget
