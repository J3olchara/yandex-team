from typing import Any, Optional, Type

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.mail import send_mail
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

# isort: off
from authorisation.models import UserProxy, ActivationToken  # noqa: I100, I101

# isort: on


class LoginBackend(ModelBackend):
    def authenticate(
        self,
        request: Optional[HttpRequest],
        username: Optional[str] = None,
        password: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[UserProxy]:
        user_model = UserProxy
        user: Optional[UserProxy]
        user = self.try_get(user_model, username=username)
        if not user:
            user = self.try_get(user_model, email__iexact=username)
        if user:
            if user.check_password(password):  # type: ignore[arg-type]
                return user
            else:
                user.profile.failed_attemps += 1
                if (
                    user.profile.failed_attemps
                    >= settings.FAILED_AUTHS_TO_DEACTIVATE
                ):
                    self.send_freeze_mail(user)
                    user.is_active = False
                    user.save()
                user.profile.save()
        return None

    @staticmethod
    def try_get(
        user_model: Type[UserProxy], **kwargs: Any
    ) -> Optional[UserProxy]:
        try:
            user = user_model.objects.get(**kwargs)
            return user
        except user_model.DoesNotExist:
            return None

    def send_freeze_mail(self, user: UserProxy) -> None:
        token = ActivationToken.objects.create(user=user)
        message = ''.join(
            (
                str(_('Дорогой ')),
                f'{user.username}',
                '!\n\n',
                str(
                    _(
                        'На вашем аккаунте обнаружена подозрительная '
                        'активность и нам пришлось его заморозить.\n'
                        'Чтобы снова получить доступ к своему '
                        'аккаунту перейдите по ссылке:\n'
                    )
                ),
                f'{token.get_url}',
            )
        )
        send_mail(
            subject=('Подозрительная активность на аккаунте!'),
            recipient_list=[user.email],
            from_email=settings.SITE_EMAIL,
            message=message,
        )
