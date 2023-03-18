"""
Feedback app tests.

Write tests here.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse
from django.test import Client, TestCase

from . import forms, models


class FeedbackFormTests(TestCase):
    def setUp(self) -> None:
        self.sender = models.Sender.objects.create(
            name='test name',
            email='test@yandex.ru',
        )
        self.feedback = models.Feedback.objects.create(
            sender=self.sender,
            text='test text',
        )
        self.feedback_file = models.FeedbackFiles.objects.create(
            file=SimpleUploadedFile('test.txt', b'test text'),
            feedback=self.feedback,
        )

    def test_feedback_page_form(self):
        """
        tests correct form view
        """
        test_path = reverse('feedback:feedback')
        fake_email = 'mail@yandex.ru'
        fake_text = 'Some question'
        fake_name = 'Billy'
        data = {
            'name': fake_name,
            'email': fake_email,
            'text': fake_text,
        }
        response = Client().post(test_path, data, follow=True)

        self.assertRedirects(
            response,
            reverse('feedback:feedback', kwargs={'feedback_status': 1}),
        )
        self.assertIn('feedback_form', response.context)

        empty_form = forms.FeedbackForm({'email': '123.123'})
        self.assertTrue(empty_form.has_error('email'))

        form: forms.FeedbackForm = response.context['feedback_form']
        self.assertEqual(len(form.visible_fields()), 4)
        for field in form.visible_fields():
            if field.name == 'email':
                self.assertEqual(field.label, 'Адрес электронной почты')
                self.assertEqual(
                    field.field.widget.attrs['placeholder'],
                    'Введите ваш email',
                )
            elif field.name == 'text':
                self.assertEqual(field.label, 'Вопрос')
                self.assertEqual(
                    field.field.widget.attrs['placeholder'], 'Опишите вопрос'
                )
            elif field.name == 'files':
                self.assertEqual(field.label, 'Приложенные файлы')
                self.assertTrue(not field.field.required)
            elif field.name == 'name':
                self.assertEqual(field.label, 'Как к вам обращаться?')
                self.assertEqual(
                    field.field.widget.attrs['placeholder'], 'Ваше имя'
                )

    def test_file_upload(self):
        """
        tests model FeedbackFiles to upload file
        """
        file = SimpleUploadedFile('test.txt', b'some text')
        models.FeedbackFiles.objects.create(
            file=file,
            feedback=self.feedback,
        )
