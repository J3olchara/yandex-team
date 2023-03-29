"""APP homepage URL Configuration"""
from typing import List

from django.urls import path, resolvers

# isort: off
from homepage import views  # noqa: I100

# isort: on

app_name = 'home'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.Home.as_view(), name='home'),
    path('coffee/', views.Coffee.as_view(), name='coffee'),
    path('test/', views.Test.as_view(), name='test'),
]
