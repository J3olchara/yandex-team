"""
Feedback app forms.

Write your forms for Feedback here.
"""
from typing import Any, List, Optional

from django import forms
from django.core.files.uploadedfile import UploadedFile

from feedback import models  # noqa: I100


class FeedbackForm(forms.ModelForm):  # type: ignore[type-arg]
    """
    Feedback Form to generate feedbacks from users

    name: char[100]. User name
    email: char[100]. User's email. validating user's email
    text: char[1000]. User feedback
    files: UploadedFile. Files for proof the text.
    """

    name = forms.CharField(
        label='Как к вам обращаться?',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ваше имя',
            }
        ),
    )

    email = forms.EmailField(
        label='Адрес электронной почты',
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Введите ваш email',
            }
        ),
    )

    text = forms.CharField(
        label='Вопрос',
        required=True,
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'class': 'form-control mb-3',
                'rows': '4',
                'placeholder': 'Опишите вопрос',
            }
        ),
    )

    files = forms.FileField(  # type: ignore[assignment]
        label='Приложенные файлы',
        required=False,
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
    )

    def save(
        self, commit: bool = True, files: Optional[List[UploadedFile]] = None
    ) -> Any:
        """
        Recreated forms.ModelForm base method to save all data to
        correct model
        name, email -> Sender;
        text, Sender.id (FK) -> Feedback;
        files, Feedback.id (FK) -> FeedbackFiles;
        """
        if files is None:
            files = []
        sender = models.Sender.objects.get_or_create(
            email=self.cleaned_data['email'],
        )[0]
        sender.name = self.cleaned_data['name']
        sender.save()
        self.instance.sender = sender
        super(FeedbackForm, self).save(commit=commit)
        if files:
            models.FeedbackFiles.objects.save_files(
                files=files, feedback=self.instance
            )
        return self.instance

    class Meta:
        model = models.Feedback

        fields = (model.text.field.name,)
        widgets = {
            model.text.field.name: forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '4',
                    'placeholder': 'Опишите вопрос',
                }
            ),
        }

    field_order = ['name', 'email', models.Feedback.text.field.name, 'files']
