"""Support functions for Core app"""
from string import punctuation


def get_normalize_table():
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
