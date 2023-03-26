"""APP homepage URL Configuration"""
from typing import List

from django.urls import path, resolvers

from . import views

app_name = 'home'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.home, name='home'),
    path('coffee/', views.coffee, name='coffee'),
    path('test/', views.test, name='test'),
]
