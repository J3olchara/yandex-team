"""CATALOG app admin settings"""
from django.contrib import admin

from . import models


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        models.Item.image_tmb,
        models.Item.name.field.name,
        models.Item.is_published.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    filter_horizontal = (
        models.Item.tags.field.name,
        models.Item.item_gallery.field.name,
    )
    list_display_links = (models.Item.name.field.name,)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
        models.Tag.slug.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = (models.Item.name.field.name,)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (
        models.Item.name.field.name,
        models.Item.is_published.field.name,
        models.Tag.slug.field.name,
    )
    list_editable = (models.Item.is_published.field.name,)
    list_display_links = (models.Item.name.field.name,)


@admin.register(models.MainImage)
class MainImageAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (models.MainImage.image.field.name,)


@admin.register(models.PhotoGallery)
class GalleryAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = (models.MainImage.image_tmb,)
