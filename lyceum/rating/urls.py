"""Rating APP urls URL Configuration"""
from typing import List

from django.urls import path, resolvers

from . import views

app_name = 'rating'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'delete/<int:item_id>/',
        views.Delete_Evaluation.as_view(),
        name='delete_evaluation',
    ),
]
