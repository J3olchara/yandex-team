"""Statistic APP urls URL Configuration"""
from typing import List

from django.urls import path, resolvers

from statistic import views

app_name = 'statistic'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'items',
        views.ItemStatistic.as_view(),
        name='item_statistic',
    ),
    path('users', views.UsersStatistics.as_view(), name='users'),
    path('rated', views.RatedStatistic.as_view(), name='rated'),
]
