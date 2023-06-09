"""Rating APP urls URL Configuration"""
from typing import List

from django.urls import path, resolvers

from rating import views

app_name = 'rating'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'delete/<int:item_id>/',
        views.DeleteEvaluation.as_view(),
        name='delete_evaluation',
    ),
]
