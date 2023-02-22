"""Support functions for Core app"""
from string import punctuation
from typing import Any, Dict, Optional


def get_normalize_table() -> Dict[str, Optional[Any]]:
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
