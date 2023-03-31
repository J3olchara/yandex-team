from datetime import date

from django.core.exceptions import ValidationError


def no_future(value: date) -> None:
    today = date.today()
    if value > today:
        raise ValidationError('Ваш день рождения не может быть в будущем.')
