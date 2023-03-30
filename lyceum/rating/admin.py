"""RATING app admin settings module"""
from django.contrib import admin

from rating import models


@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model tags table"""

    list_display = (models.Evaluation.value.field.name,)
