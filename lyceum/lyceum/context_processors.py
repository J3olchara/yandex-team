"""
Context processor

creates some variables for all templates
"""
from datetime import date
from typing import Any, Dict

import authorisation.models as auth_models
from django.http import HttpRequest


def today_birthday_processor(request: HttpRequest) -> Dict[str, Any]:
    today = date.today()
    return {
        'today_birthdays': auth_models.Profile.objects.filter(
            birthday__day=today.day, birthday__month=today.month
        )
    }
