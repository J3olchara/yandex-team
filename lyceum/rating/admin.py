"""RATING app admin settings module"""
from django.contrib import admin

# isort: off
from rating import models  # noqa: I100

# isort: on


# mypy: disable-error-code="attr-defined"
@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model tags table"""

    list_display = (models.Evaluation.value.field.name,)
