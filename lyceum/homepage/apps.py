"""APP homepage config"""
from django.apps import AppConfig


class HomepageConfig(AppConfig):
    """Class app config"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'
    verbose_name = 'Основная страница'
