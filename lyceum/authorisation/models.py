import uuid
from datetime import date, datetime
from typing import Any, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from pytz import timezone, utc

from . import utils


class Profile(models.Model):
    user: Union[User, Any] = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
    )

    birthday: Union[date, Any] = models.DateField(
        verbose_name='дата рождения',
        null=True,
        blank=True,
    )

    avatar: Any = models.ImageField(
        verbose_name='аватар',
        default='uploads/cat.jpg',
        upload_to=utils.get_avatar_path,
        null=True,
        blank=True,
    )

    coffee_count: Union[int, Any] = models.IntegerField(
        verbose_name='попыток сварить кофе',
        default=0,
        blank=False,
        null=False,
    )

    about: Union[str, Any] = models.TextField(
        verbose_name='О пользователе',
        null=True,
        blank=True,
    )

    def coffee_break(self) -> None:
        self.coffee_count += 1
        self.save()

    class Meta:
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'


class UserManagerExtended(models.Manager):  # type: ignore[type-arg]
    def get_queryset(self) -> Any:
        return (
            super(UserManagerExtended, self)
            .get_queryset()
            .select_related('profile')
        )


class UserProxy(User):

    objects = UserManagerExtended()  # type: ignore[assignment]

    class Meta:
        proxy = True


class ActivationToken(models.Model):
    user: Union[User, Any] = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    token: Union[uuid.UUID, Any] = models.UUIDField(
        verbose_name='Ключ активации', default=uuid.uuid4
    )

    created: Union[datetime, Any] = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True,
    )

    expire: Union[datetime, Any] = models.DateTimeField(
        verbose_name='Дата и время истечения',
        default=utils.get_token_expire,
    )

    def get_url(self, site: str) -> Any:
        return site + reverse(
            'authorisation:signup_confirm',
            kwargs={'user_id': self.user.id, 'token': self.token},
        )

    def expired(self) -> bool:
        tz = timezone(settings.TIME_ZONE)
        expire = self.expire.replace(tzinfo=utc).astimezone(tz)
        exp = expire < datetime.now(tz=tz)
        if exp:
            self.delete()
        return exp
