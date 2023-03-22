import django.contrib.auth.forms as default_forms
import django.contrib.auth.views as default_views
import django.urls

from . import forms, views

app_name = 'authorisation'

urlpatterns = [
    django.urls.path(
        'login/',
        views.CustomLoginView.as_view(),
        name='login',
    ),
    django.urls.path(
        'logout/',
        default_views.LogoutView.as_view(
            template_name='homepage/index.html',
        ),
        name='logout',
    ),
    django.urls.path(
        'password_change/',
        default_views.PasswordChangeView.as_view(
            template_name='users/password_change.html',
            form_class=forms.PasswordChangeForm,
        ),
        name='password_change',
    ),
    django.urls.path(
        'password_change/done/',
        views.CustomChangePasswordDone.as_view(),
        name='password_change_done',
    ),
    django.urls.path(
        'password_reset/',
        default_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            form_class=forms.PasswordResetForm,
        ),
        name='password_reset',
    ),
    django.urls.path(
        'password_reset/done/',
        views.CustomPasswordResetDone.as_view(),
        name='password_reset_done',
    ),
    django.urls.path(
        'reset/<uidb64>/<token>/',
        default_views.PasswordResetConfirmView.as_view(
            template_name='users/password_change.html',
            form_class=forms.PasswordResetConfirmForm,
        ),
        name='password_reset_confirm',
    ),
    django.urls.path(
        'reset/done/',
        views.CustomPasswordResetComplete.as_view(),
        name='password_reset_complete',
    ),
    django.urls.path(
        'signup/',
        views.signup,
        name='signup',
    ),
    django.urls.path('signup/done/', views.signup_done, name='signup_done'),
    django.urls.path(
        'signup/<nat:user_id>/<uuid:token>/',
        views.signup_confirm,
        name='signup_confirm',
    ),
]
