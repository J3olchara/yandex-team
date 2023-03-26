"""Rating APP urls URL Configuration"""
from typing import List

from django.urls import path, resolvers

from . import views


app_name = 'rating'

urlpatterns: List[resolvers.URLPattern] = [
    path(
        'delete/<int:user_id>/<int:item_id>',
        views.delete_evaluation,
        name='delete_evaluation',
    ),
]
