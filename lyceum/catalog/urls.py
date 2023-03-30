"""Catalog APP urls URL Configuration"""
from typing import List

from django.urls import path, re_path, register_converter, resolvers

# isort: off
from catalog import converters, views  # noqa: I100

# isort: on

register_converter(converters.NaturalNumber, 'nat')

app_name = 'catalog'

urlpatterns: List[resolvers.URLPattern] = [
    path('', views.ItemList.as_view(), name='catalog'),
    path(
        '<int:item_id>/',
        views.ItemDetailView.as_view(),
        name='int_item_detail',
    ),
    re_path(
        r'^re/(?P<item_id>[1-9]\d*)/$',
        views.RegularItem.as_view(),
        name='re_item_detail',
    ),
    path(
        'converter/<nat:item_id>/',
        views.ConverterItem.as_view(),
        name='conv_item_detail',
    ),
    path('news/', views.News.as_view(), name='news'),
    path('friday/', views.Friday.as_view(), name='friday'),
    path('unchecked/', views.Unchecked.as_view(), name='unchecked'),
]
