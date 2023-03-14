from typing import List, Union

from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile, UploadedFile
from django.db import models
from django_cleanup import cleanup

from . import support


class Sender(models.Model):
    name = models.CharField(
        verbose_name='Имя',
        max_length=100,
    )

    email = models.EmailField(
        verbose_name='электронная почта',
        unique=True,
    )

    first_feedback = models.DateTimeField(
        auto_now_add=True,
    )


class FeedbackManager(models.Manager):  # type: ignore[type-arg]
    def create_feedback(
        self,
        name: str,
        email: str,
        text: str,
        files: Union[List[UploadedFile], SimpleUploadedFile],
    ) -> None:
        mail.send_mail(
            subject=f'Feedback from {name}',
            from_email=email,
            message=text,
            recipient_list=['yoursite@gmail.com'],
        )
        qs = Sender.objects.filter(email=email)
        if not qs:
            sender = Sender.objects.create(
                name=name,
                email=email,
            )
        else:
            sender = qs[0]
        feedback = self.create(
            sender=sender,
            text=text,
        )
        for file in files:
            FeedbackFiles.objects.create(file=file, feedback=feedback)


class Feedback(models.Model):
    objects = FeedbackManager()

    sender = models.ForeignKey(
        Sender,
        on_delete=models.DO_NOTHING,
        verbose_name='Отправитель',
    )

    text = models.TextField(
        verbose_name='Текст',
    )

    process_choices = (
        ('received', 'получено'),
        ('processing', 'в обработке'),
        ('answered', 'ответ дан'),
    )

    processing_status = models.CharField(
        default=process_choices[0][0],
        choices=process_choices,
        blank=False,
        max_length=100,
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True,
    )


@cleanup.select
class FeedbackFiles(models.Model):
    feedback = models.ForeignKey(
        'Feedback',
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to=support.make_file_path,
    )
