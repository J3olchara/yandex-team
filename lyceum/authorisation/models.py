import uuid
from datetime import datetime, timedelta
from pytz import timezone

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import reverse

from . import utils


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        related_name='profile',
        on_delete=models.CASCADE,
    )

    birthday = models.DateField(
        verbose_name='дата рождения',
        null=True,
        blank=True,
    )

    avatar = models.ImageField(
        verbose_name='аватар',
        default='uploads/cat.jpg',
        null=True,
        blank=True,
    )

    coffee_count = models.IntegerField(
        verbose_name='попыток сварить кофе',
        default=0,
        blank=False,
        null=False,
    )

    about = models.TextField(
        verbose_name='О пользователе',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'


class UserManagerExtended(models.Manager):
    def get_queryset(self):
        return (
            super(UserManagerExtended, self)
            .get_queryset()
            .select_related('profile')
        )


class UserProxy(get_user_model()):

    objects = UserManagerExtended()

    class Meta:
        proxy = True


class ActivationToken(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )

    token = models.UUIDField(verbose_name='Ключ активации', default=uuid.uuid4)

    created = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True,
    )

    expire = models.DateTimeField(
        verbose_name='Дата и время истечения',
        default=utils.get_token_expire,
    )

    def get_url(self, site):
        return site + reverse(
            'authorisation:signup_confirm',
            kwargs={'user_id': self.user.id, 'token': self.token},
        )

    def expired(self):
        exp = self.expire.replace(tzinfo=timezone(settings.TIME_ZONE)) < datetime.now(tz=timezone(settings.TIME_ZONE))
        if exp:
            self.delete()
        return exp
