"""Catalog APP urls URL Configuration"""
from typing import List

from django.urls import path, re_path, register_converter, resolvers

from . import converters, views

register_converter(converters.NaturalNumber, 'nat')

app_name = 'catalog'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.item_list, name='catalog'),
    path('<int:item_id>/', views.item_detail, name='int_item_detail'),
    re_path(
        r'^re/(?P<item_id>[1-9]\d*)/$',
        views.regular_item,
        name='re_item_detail',
    ),
    path(
        'converter/<nat:item_id>/',
        views.converter_item,
        name='conv_item_detail',
    ),
    path('news/', views.news, name='news'),
    path('friday/', views.friday, name='friday'),
    path('unchecked/', views.unchecked, name='unchecked'),
]
