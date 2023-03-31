"""
Context processor

creates some variables for all templates
"""
from typing import Any, Dict

from django.http import HttpRequest
from django.utils.timezone import datetime

import authorisation.models as auth_models


def today_birthday_processor(request: HttpRequest) -> Dict[str, Any]:
    today = datetime.today()
    return {
        'today_birthdays': auth_models.Profile.objects.filter(
            birthday__day=today.day,
            birthday__month=today.month,
            birthday__year__lte=today.year,
        )
    }
