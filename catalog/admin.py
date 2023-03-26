"""CATALOG app admin settings"""
from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model tags table"""

    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
        models.Tag.slug.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = (models.Item.name.field.name,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model for Category table"""

    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
        models.Tag.slug.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = (models.Item.name.field.name,)


class GalleryItemInline(admin.TabularInline):  # type: ignore[type-arg]
    """Admin inline model for Item PhotoGallery"""

    model = models.PhotoGallery


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model for Item"""

    list_display = (
        models.Item.image_tmb,
        models.Item.name.field.name,
        models.Item.is_published.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    filter_horizontal = (models.Item.tags.field.name,)
    list_display_links = (models.Item.name.field.name,)
    inlines = [
        GalleryItemInline,
    ]
