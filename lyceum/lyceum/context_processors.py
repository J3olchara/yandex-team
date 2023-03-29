"""
Context processor

creates some variables for all templates
"""
from typing import Any, Dict

import authorisation.models as auth_models
from django.http import HttpRequest
from django.utils.timezone import datetime


def today_birthday_processor(request: HttpRequest) -> Dict[str, Any]:
    today = datetime.today()
    return {
        'today_birthdays': auth_models.Profile.objects.filter(
            birthday__day=today.day, birthday__month=today.month
        )
    }
