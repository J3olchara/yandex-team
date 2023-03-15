import datetime
from typing import Any, List, Union

from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django_cleanup import cleanup

from . import support


class Sender(models.Model):
    name: Union[str, 'models.CharField[Any, Any]'] = models.CharField(
        verbose_name='Имя',
        max_length=100,
    )

    email: Union[str, 'models.EmailField[Any, Any]'] = models.EmailField(
        verbose_name='электронная почта',
        unique=True,
    )

    first_feedback: Union[
        str, 'models.DateTimeField[Any, Any]'
    ] = models.DateTimeField(
        auto_now_add=True,
    )


class Feedback(models.Model):
    objects = models.Manager()

    sender: Union[Sender, 'models.ForeignKey[Any, Any]'] = models.ForeignKey(
        Sender,
        on_delete=models.PROTECT,
        verbose_name='Отправитель',
    )

    text: Any = models.TextField(
        verbose_name='Текст',
    )

    process_choices = (
        ('received', 'получено'),
        ('processing', 'в обработке'),
        ('answered', 'ответ дан'),
    )

    processing_status: Union[
        str, 'models.CharField[Any, Any]'
    ] = models.CharField(
        default=process_choices[0][0],
        choices=process_choices,
        blank=False,
        max_length=100,
    )

    created_at: Union[
        datetime.datetime, 'models.DateTimeField[Any, Any]'
    ] = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True,
    )


class FeedbackFilesManager(models.Manager['FeedbackFiles']):
    def save_files(
        self, files: List[UploadedFile], feedback: Feedback
    ) -> None:
        feedback_files_list = [
            FeedbackFiles(file=file, feedback=feedback) for file in files
        ]
        self.bulk_create(feedback_files_list)


@cleanup.select
class FeedbackFiles(models.Model):
    objects = FeedbackFilesManager()

    feedback: Union[
        'Feedback', 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
        'Feedback',
        on_delete=models.CASCADE,
    )
    file: Union[UploadedFile, 'models.FileField'] = models.FileField(
        upload_to=support.make_file_path,
    )
