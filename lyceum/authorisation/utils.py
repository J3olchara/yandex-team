from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from pytz import timezone

from . import models


def get_token_expire() -> datetime:
    """Creates expire time for the activation token."""
    days, time = settings.ACTIVATION_URL_EXPIRE_TIME.split()
    expire = datetime.strptime(time, '%H:%M')
    return datetime.now(tz=timezone(settings.TIME_ZONE)) + timedelta(
        days=int(days),
        hours=expire.hour,
        minutes=expire.minute,
        seconds=expire.second,
    )


def get_avatar_path(instance: 'models.Profile', filename: str) -> str:
    """returns path to upload user avatar"""
    return f'uploads/avatars/{uuid4()}.{filename.split(maxsplit=1)[-1]}'
