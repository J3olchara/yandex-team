from django.contrib.auth.models import User, AbstractUser
from django.db import models


class Profile(User):
    user = models.OneToOneField(
        User,
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

    def __str__(self):
        return self.user.username[:10]

    class Meta:
        proxy = True
        verbose_name = 'Дополнительное поле'
        verbose_name_plural = 'Дополнительные поля'