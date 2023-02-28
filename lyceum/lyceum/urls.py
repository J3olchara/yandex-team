"""lyceum URL Configuration"""
from typing import Any

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns: Any = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('homepage.urls')),
    path('catalog/', include('catalog.urls')),
    path('about/', include('about.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar.urls

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
