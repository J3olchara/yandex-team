"""RATING app database models"""
from typing import Any

import django.core.validators
from django.db import models

# isort: off
import catalog.models  # noqa: I100
import authorisation.models

# isort: on


class Evaluation(models.Model):
    user: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        authorisation.models.UserProxy, on_delete=models.CASCADE
    )
    item: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        catalog.models.Item, on_delete=models.CASCADE
    )

    value = models.PositiveSmallIntegerField(
        'оценка',
        validators=[
            django.core.validators.MaxValueValidator(
                5, message='Максимальное значение оценки - 5'
            ),
            django.core.validators.MinValueValidator(
                1, message='Минимальное значение оценки - 1'
            ),
        ],
    )

    change_datetime = models.DateTimeField(
        verbose_name='дата и время изменения',
        help_text='значение обновляется каждый раз, '
        'когда пользователь меняет свою оценку',
        auto_now=True,
    )

    creation_datetime = models.DateTimeField(
        verbose_name='дата и время создания',
        help_text='дата и время создания отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
