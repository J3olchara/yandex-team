"""APP urls URL Configuration"""
from typing import List

from django.urls import path, resolvers

from . import views

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.item_list),
    path('<int:item_id>/', views.item_detail),
]
