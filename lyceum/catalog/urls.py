"""APP urls URL Configuration"""
from typing import List

from django.urls import path, resolvers

from . import views

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.item_list),
    path('<int:pk>/', views.item_detail),
]
