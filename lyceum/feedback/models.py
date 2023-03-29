"""
Feedback app models

Create your database models for Feedback here.
"""
import datetime
from typing import Any, List, Union

from django.core.files.uploadedfile import UploadedFile
from django.db import models
from django_cleanup import cleanup

from feedback import support  # noqa: I100


class Sender(models.Model):
    """
    Sender model to save users data.

    name: char[100]. User name.
    email: char[254]. User email. Validate email.
    first_feedback: datetime.datetime. First feedback datetime.
    """

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


@cleanup.select
class Feedback(models.Model):
    """
    Feedback model to save feedbacks.

    sender: id FK -> Sender.
    text: str. Feedback main text body.
    processing_status: char[100] choice <- process_choices
    created_at: datetime.datetime. Feedback creation date
    """

    objects = models.Manager()

    process_choices = (
        ('received', 'получено'),
        ('processing', 'в обработке'),
        ('answered', 'ответ дан'),
    )

    sender: Union[Sender, 'models.ForeignKey[Any, Any]'] = models.ForeignKey(
        Sender,
        on_delete=models.PROTECT,
        verbose_name='Отправитель',
    )

    text: Any = models.TextField(
        verbose_name='Текст',
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
    """
    Feedback files manager to manage fedback files save.
    """

    def save_files(
        self, files: List[UploadedFile], feedback: Feedback
    ) -> None:
        """
        saves more than one file
        """
        feedback_files_list = [
            FeedbackFiles(file=file, feedback=feedback) for file in files
        ]
        self.bulk_create(feedback_files_list)


@cleanup.select
class FeedbackFiles(models.Model):
    """
    Feedback files to save feedback files (some feedback proof).

    feedback: id FK -> Feedback. Feedback that contains this file.
    file: UploadedFile. Feedback file proof.
    """

    objects = FeedbackFilesManager()

    feedback: Union[
        'Feedback', 'models.ForeignKey[Any, Any]'
    ] = models.ForeignKey(
        'Feedback',
        on_delete=models.CASCADE,
    )
    file: Union[UploadedFile, 'models.FileField'] = models.FileField(
        upload_to=support.make_feedback_files_path,
    )
