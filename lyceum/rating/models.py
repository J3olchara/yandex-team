"""RATING app database models"""
from typing import Any

import django.core.validators
from django.db import models

# isort: off
import authorisation.models  # noqa: I100
import catalog.models  # noqa: I100

# isort: on


class Evaluation(models.Model):
    user: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        authorisation.models.UserProxy,
        verbose_name='пользователь',
        help_text='Пользователь оставивший отзыв',
        on_delete=models.CASCADE,
    )
    item: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        catalog.models.Item,
        verbose_name='товар',
        help_text='товар, которому оставили отзыв',
        on_delete=models.CASCADE,
    )

    value = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        help_text='значение оценки',
        validators=[
            django.core.validators.MaxValueValidator(
                5, message='Максимальное значение оценки - 5'
            ),
            django.core.validators.MinValueValidator(
                1, message='Минимальное значение оценки - 1'
            ),
        ],
    )

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
