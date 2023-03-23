from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(
    post_save, sender=models.UserProxy, dispatch_uid='save_new_user_profile'
)
def save_profile(
    sender: Any, instance: models.UserProxy, created: bool, **kwargs: Any
) -> None:
    if created:
        profile = models.Profile(user=instance)
        profile.save()


@receiver(
    post_save, sender=models.UserProxy, dispatch_uid='normalize_user_email'
)
def normalize_email(
    sender: Any, instance: models.UserProxy, **kwargs: Any
) -> None:
    if instance.email:
        instance.profile.normalize_email()
        instance.profile.save()
