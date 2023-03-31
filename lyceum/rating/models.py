"""RATING app database models"""
from typing import Any

import django.core.validators
from django.db import models

import authorisation.models
import catalog.models
from catalog.models import Tag


class EvaluationManager(models.Manager['Evaluation']):
    def get_item(self, **kwargs):
        prefetch = models.Prefetch(
            'item__tags',
            queryset=Tag.objects.filter(is_published=True).only(
                'name',
            ),
        )
        return (
            self.get_queryset()
            .filter(**kwargs)
            .select_related('item__category')
            .prefetch_related(prefetch)
            .only(
                'item__id',
                'item__name',
                'item__text',
                'item__category__name',
                'item__image',
                'item__tags__name',
            )
        )


class Evaluation(models.Model):
    """
    Evaluation model to rate items

    user: int FK -> authorisation.models.UserProxy.
                    User that leaved this evaluation.
    item: int FK -> catalog.models.Item.
                    Item that user rated.
    value: int [1;5].
                    the rating given by the user.
    """

    objects = EvaluationManager()

    user: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        authorisation.models.UserProxy,
        verbose_name='пользователь',
        help_text='Пользователь оставивший отзыв',
        related_name='evaluations',
        on_delete=models.CASCADE,
    )
    item: 'models.ForeignKey[Any, Any]' = models.ForeignKey(
        catalog.models.Item,
        verbose_name='товар',
        help_text='Товар, которому оставили отзыв',
        related_name='rating_item',
        on_delete=models.CASCADE,
    )

    value = models.PositiveSmallIntegerField(
        verbose_name='оценка',
        help_text='Значение оценки',
        validators=[
            django.core.validators.MaxValueValidator(
                5, message='Максимальное значение оценки - 5'
            ),
            django.core.validators.MinValueValidator(
                1, message='Минимальное значение оценки - 1'
            ),
        ],
    )

    changed = models.DateTimeField(
        verbose_name='последнее изменение',
        help_text='Когда был изменён в последний раз',
        auto_now=True,
    )

    created = models.DateTimeField(
        verbose_name='Создан',
        help_text='Когда был создан',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'
