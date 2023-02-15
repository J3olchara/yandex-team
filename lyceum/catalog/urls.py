"""APP urls URL Configuration"""
from typing import List

from django.urls import path, re_path, register_converter, resolvers

from . import converters, views

register_converter(converters.NaturalNumber, 'nat')

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.item_list, name='catalog'),
    path('<int:item_id>/', views.item_detail, name='int_item_deatil'),
    re_path(r'^re/[1-9]\d*/', views.regular_item, name='re_item_deatil'),
    path(
        'converter/<nat:item_id>/',
        views.converter_item,
        name='conv_item_deatil',
    ),
]
