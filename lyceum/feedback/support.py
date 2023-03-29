"""
Feedback support functions

Write your support functions here.
"""
from uuid import uuid4

from django.conf import settings

# isort: off
from feedback import models  # noqa: I100

# isort: on


def make_feedback_files_path(
    instance: 'models.FeedbackFiles', filename: str
) -> str:
    """
    Creates file path for unique sender and feedback
    """
    file_format = filename.split('.', maxsplit=1)[-1]
    path = (
        settings.FEEDBACK_URL
        + rf'user_{instance.feedback.sender.id}\\'
        + rf'feedback_{instance.feedback.id}\\'
        + rf'{uuid4()}.{file_format}'
    )
    return path
