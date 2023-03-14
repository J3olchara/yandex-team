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
        test_path = reverse('feedback:feedback')
        fake_email = 'mail@yandex.ru'
        fake_text = 'Some question'
        fake_name = 'Billy'
        data = {
            'name': fake_name,
            'email': fake_email,
            'text': fake_text,
        }
        request = Client().post(test_path, data)
        self.assertIn('feedback_form', request.context)
        form: forms.FeedbackForm = request.context['feedback_form']
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
        # тест на редирект не стал делать ибо его вообще тут нет
        # потому что а зачем тут редирект вообще в этой вьюхе
        # можно же просто после отправки прогрузить страницу как я и сделал
        sender = models.Sender.objects.get(email=form.data['email'])
        models.Feedback.objects.get(sender=sender, text=form.data['text'])

    def test_file_upload(self):
        file = SimpleUploadedFile('test.txt', b'some text')
        models.FeedbackFiles.objects.create(
            file=file,
            feedback=self.feedback,
        )
