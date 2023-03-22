from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save

from . import models


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    if created:
        profile = models.Profile(user=instance)
        profile.save()
