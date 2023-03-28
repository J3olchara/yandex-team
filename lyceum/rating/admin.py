"""RATING app admin settings module"""
from django.contrib import admin

from . import models


# mypy: disable-error-code="attr-defined"
@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model tags table"""

    list_display = (models.Evaluation.value.field.name,)
