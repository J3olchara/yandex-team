"""lyceum URL Configuration"""
from typing import List

from django.contrib import admin
from django.urls import include, path, resolvers

from . import settings

urlpatterns: List[resolvers.URLResolver] = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('catalog/', include('catalog.urls')),
    path('about/', include('about.urls')),
]


if settings.DEBUG:
    import debug_toolbar.urls

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
