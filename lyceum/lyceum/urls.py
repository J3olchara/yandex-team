"""lyceum URL Configuration"""
from typing import Any

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

# isort: off
import about.urls
import authorisation.urls
import catalog.urls
import django.contrib.auth.urls
import django.urls
import feedback.urls
import homepage.urls
import users.urls

# isort: on

urlpatterns: Any = [
    django.urls.path('admin/', admin.site.urls, name='admin'),
    django.urls.path(
        'ckeditor/', django.urls.include('ckeditor_uploader.urls')
    ),
    django.urls.path('i18n/', django.urls.include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    django.urls.path('', django.urls.include(homepage.urls)),
    django.urls.path('catalog/', django.urls.include(catalog.urls)),
    django.urls.path('about/', django.urls.include(about.urls)),
    django.urls.path('feedback/', django.urls.include(feedback.urls)),
    django.urls.path('auth/', django.urls.include(authorisation.urls)),
    django.urls.path('auth/', django.urls.include(django.contrib.auth.urls)),
    django.urls.path('users/', django.urls.include(users.urls)),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar.urls

    urlpatterns += [
        django.urls.path(
            '__debug__/', django.urls.include(debug_toolbar.urls)
        ),
    ]
