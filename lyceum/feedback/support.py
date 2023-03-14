from uuid import uuid4

from . import models


def make_file_path(instance: 'models.FeedbackFiles', filename: str) -> str:
    file_format = filename.split('.', maxsplit=1)[-1]
    path = (
        rf'uploads\\feedback\\user_{instance.feedback.sender.id}\\'
        + rf'feedback_{instance.feedback.id}\\{uuid4()}.{file_format}'
    )
    return path
