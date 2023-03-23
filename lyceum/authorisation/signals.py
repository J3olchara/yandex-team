from typing import Any

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(
    sender: Any, instance: Any, created: bool, **kwargs: Any
) -> Any:
    if created:
        profile = models.Profile(user=instance)
        profile.save()
