"""APP urls URL Configuration"""
from typing import List

from django.urls import path, re_path, register_converter, resolvers

from . import converters, views

register_converter(converters.NaturalNumber, 'nat')

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.item_list),
    path('<int:item_id>/', views.item_detail),
    re_path(r'^re/[1-9]\d*/', views.regular_item),
    path('converter/<nat:item_id>/', views.converter_item),
]
