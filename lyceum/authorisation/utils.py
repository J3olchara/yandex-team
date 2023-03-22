from datetime import datetime, timedelta
from pytz import timezone

from django.conf import settings


def get_token_expire() -> datetime:
    days, time = settings.ACTIVATION_URL_EXPIRE_TIME.split()
    expire = datetime.strptime(
        time, '%H:%M'
    )
    return datetime.now(tz=timezone(settings.TIME_ZONE)) + timedelta(
        days=int(days),
        hours=expire.hour,
        minutes=expire.minute,
        seconds=expire.second,
    )
