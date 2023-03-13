from django.db import models


class Feedback(models.Model):
    email = models.EmailField(
        verbose_name='Электронная почта',
    )

    text = models.TextField(
        verbose_name='Текст',
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now=True,
    )
