"""
Support definitions for core

contains defiunitions that helps core module
"""
from string import punctuation
from typing import Any, Dict, Optional
from uuid import uuid4

from django.conf import settings


def get_normalize_table() -> Dict[str, Optional[Any]]:
    """
    returns table for name-normalizing in model Item

    replaces all russian letters that simplify
    english letters to english letter and deletes
    all punctuation from string.
    """
    tab = dict.fromkeys(punctuation)
    alphabet = {  # rus: eng
        'А': 'A',
        'В': 'B',
        'Е': 'E',
        'Т': 'T',
        'О': 'O',
        'Р': 'P',
        'Н': 'H',
        'К': 'K',
        'Х': 'X',
        'С': 'C',
        'М': 'M',
        ' ': '',
    }
    tab.update(alphabet)
    return tab


path_mapping = {
    'Item': 'uploads/catalog/items_gallery',
    'PhotoGallery': 'uploads/catalog/items_gallery',
}


def get_upload_location(instance: Any, filename: str) -> str:
    """
    Returns directory to upload file from
    some model file field

    all paths that mapping files is in path_mapping
    'ModelClassName': 'path/from/media'
    """
    global path_mapping
    try:
        path = path_mapping[instance.__class__.__name__]
    except KeyError:
        path = 'Unknown'
    name = str(uuid4()) + f'.{filename.split(".")[-1]}'
    return str(settings.MEDIA_ROOT / path / name)
