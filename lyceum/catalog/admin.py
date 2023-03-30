"""CATALOG app admin settings"""
from django.contrib import admin

import catalog.models  # noqa: I100


@admin.register(catalog.models.Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model tags table"""

    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Tag.slug.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)


@admin.register(catalog.models.Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model for Category table"""

    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Tag.slug.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)


class GalleryItemInline(admin.TabularInline):  # type: ignore[type-arg]
    """Admin inline model for Item PhotoGallery"""

    model = catalog.models.PhotoGallery


@admin.register(catalog.models.Item)
class ItemAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    """Admin model for Item"""

    list_display = (
        catalog.models.Item.image_tmb,
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    inlines = [
        GalleryItemInline,
    ]
