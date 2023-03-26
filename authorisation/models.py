import uuid
from datetime import date, datetime
from typing import Any, Union

from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from pytz import timezone, utc

from . import utils


class Profile(models.Model):
    user: Union[User, Any] = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )

    birthday: Union[date, Any] = models.DateField(
        verbose_name=_('дата рождения'),
        null=True,
        blank=True,
    )

    avatar: Any = models.ImageField(
        verbose_name=_('аватар'),
        default='uploads/cat.jpg',
        upload_to=utils.get_avatar_path,
        null=True,
        blank=True,
    )

    coffee_count: Union[int, Any] = models.IntegerField(
        verbose_name=_('попыток сварить кофе'),
        default=0,
        blank=False,
        null=False,
    )

    about: Union[str, Any] = models.TextField(
        verbose_name=_('О пользователе'),
        null=True,
        blank=True,
    )

    normalized_email: Union[str, Any] = models.EmailField(
        verbose_name=_('Нормализованная почта'),
        null=True,
        blank=True,
    )

    failed_attemps: Union[int, Any] = models.PositiveSmallIntegerField(
        verbose_name=_('Неудачных попыток входа подряд'), default=0
    )

    def normalize_email(self) -> str:
        name, domain = strip_tags(self.user.email).lower().split('@')
        domain = domain.replace('ya.ru', 'yandex.ru')
        if domain == 'gmail.com':
            name = name.replace('.', '')
        elif domain == 'yandex.ru':
            name = name.replace('.', '-')
        self.normalized_email = '@'.join([name, domain])
        return self.normalized_email

    def coffee_break(self) -> None:
        self.coffee_count += 1
        self.save()

    class Meta:
        verbose_name = _('Дополнительное поле')
        verbose_name_plural = _('Дополнительные поля')


class UserManagerExtended(UserManager['UserProxy']):
    def get_queryset(self) -> Any:
        return (
            super(UserManagerExtended, self)
            .get_queryset()
            .select_related('profile')
            .filter(is_active=True)
        )


class InactiveUserManagerExtended(UserManager['UserProxy']):
    def get_queryset(self) -> Any:
        return (
            super(InactiveUserManagerExtended, self)
            .get_queryset()
            .select_related('profile')
        )


class UserProxy(User):
    objects = UserManagerExtended()  # type: ignore[assignment]
    inactive = InactiveUserManagerExtended()

    class Meta:
        proxy = True


class ActivationToken(models.Model):
    user: Union[User, Any] = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Пользователь'),
    )

    token: Union[uuid.UUID, Any] = models.UUIDField(
        verbose_name=_('Ключ активации'), default=uuid.uuid4
    )

    created: Union[datetime, Any] = models.DateTimeField(
        verbose_name=_('Дата и время создания'),
        auto_now_add=True,
    )

    expire: Union[datetime, Any] = models.DateTimeField(
        verbose_name=_('Дата и время истечения'),
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
