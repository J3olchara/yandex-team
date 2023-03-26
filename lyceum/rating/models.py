"""RATING app database models"""
from django.db import models
from typing import Union, Any
import catalog.models
import authorisation.models
import django.core.validators


class Evaluation(models.Model):
    user: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        authorisation.models.User, on_delete=models.CASCADE
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
                1, message='Минимальное значение оценки - 1ы'
            ),
        ],
    )

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
