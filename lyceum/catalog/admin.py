"""CATALOG app admin settings"""
from django.contrib import admin
from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
    )
    list_editable = (
        models.Item.is_published.field.name,
    )
    # list_display_links = (
    #     'id',
    # )


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        models.Item.is_published.field.name,
        'id',
        models.Item.name.field.name,
        models.Tag.slug.field.name,
    )
    list_editable = (
        models.Item.is_published.field.name,
        models.Item.name.field.name,
    )
    list_display_links = (
        'id',
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        models.Item.is_published.field.name,
        'id',
        models.Item.name.field.name,
        models.Tag.slug.field.name,
    )
    list_editable = (
        models.Item.is_published.field.name,
        models.Item.name.field.name,
    )
    list_display_links = (
        'id',
    )
