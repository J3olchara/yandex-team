"""RATING app admin settings module"""
from django.contrib import admin


from . import models


@admin.register(models.Evaluation)
class TagAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model tags table"""

    list_display = (
        models.Evaluation.value.field.name,
    )
