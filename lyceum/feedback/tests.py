from django.shortcuts import reverse
from django.test import Client, TestCase

from . import forms


class FeedbackFormTests(TestCase):
    def test_form_context(self):
        test_path = reverse('feedback:feedback')
        fake_email = 'mail@yandex.ru'
        fake_text = 'Some question'
        data = {
            'email': fake_email,
            'text': fake_text,
        }
        request = Client().post(test_path, data)
        self.assertIn('feedback_form', request.context)
        form: forms.FeedbackForm = request.context['feedback_form']
        self.assertEqual(len(form.visible_fields()), 2)
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
        # тест на редирект не стал делать
        # потому что а зачем тут редирект вообще в этой вьюхе
