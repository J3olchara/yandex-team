"""APP about URL Configuration"""
from typing import List

from django.urls import path, resolvers

from . import views

app_name = 'about'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.description, name='about'),
]
