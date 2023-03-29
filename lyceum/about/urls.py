"""APP about URL Configuration"""
from typing import List

from django.urls import path, resolvers

import about.views  # noqa: I100

app_name = 'about'

urlpatterns: List[resolvers.URLPattern] = [
    path('', about.views.Description.as_view(), name='about'),
]
