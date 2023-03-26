"""APP catalog config"""
from django.apps import AppConfig


class CatalogConfig(AppConfig):
    """Class app config"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalog'
    verbose_name = 'Каталог'
