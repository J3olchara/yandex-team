"""RATING app database models"""
from typing import Any

import authorisation.models
import catalog.models
import django.core.validators
from django.db import models


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

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
