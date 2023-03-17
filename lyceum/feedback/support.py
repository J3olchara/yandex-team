"""
Feedback support functions

Write your support functions here.
"""
from uuid import uuid4

from . import models


def make_feedback_files_path(
    instance: 'models.FeedbackFiles', filename: str
) -> str:
    """
    Creates file path for unique sender and feedback
    """
    file_format = filename.split('.', maxsplit=1)[-1]
    path = (
        rf'uploads\\feedback\\user_{instance.feedback.sender.id}\\'
        + rf'feedback_{instance.feedback.id}\\{uuid4()}.{file_format}'
    )
    return path
