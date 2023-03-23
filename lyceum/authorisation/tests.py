from datetime import timedelta
from unittest import mock

from django.contrib.auth.hashers import make_password
from django.shortcuts import reverse
from django.test import Client, TestCase, override_settings
from parameterized import parameterized

from . import forms, models


class SignUpTests(TestCase):
    def setUp(self) -> None:
        self.user = models.UserProxy.objects.create(
            username='some_test_username_qwerty',
            password=make_password('empty_password'),
            email='danila_eremin_email@google.comtest',
            is_active=False,
        )
        self.user_password = 'empty_password'
        self.token = models.ActivationToken.objects.create(user=self.user)

    def test_signup_endpoint(self):
        path = reverse('authorisation:signup')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_signup_done_endpoint(self):
        path = reverse('authorisation:signup_done')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    @mock.patch('authorisation.models.datetime')
    def test_activation_false(self, mocked_datetime):
        path = reverse(
            'authorisation:signup_confirm',
            kwargs={'token': self.token.token, 'user_id': self.user.id},
        )
        mocked_datetime.now.return_value = self.token.expire + timedelta(
            minutes=1
        )
        resp = Client().get(path)
        self.user = models.UserProxy.inactive.get(id=self.user.id)
        self.assertIn('alerts', resp.context)
        self.assertEqual(
            'danger',
            resp.context['alerts'][0]['type'],
            resp.context['alerts'][0]['text'],
        )
        self.assertTrue(not self.user.is_active, self.user.is_active)

    @mock.patch('authorisation.models.datetime')
    def test_activation_true(self, mocked_datetime):
        path = reverse(
            'authorisation:signup_confirm',
            kwargs={'token': self.token.token, 'user_id': self.user.id},
        )
        mocked_datetime.now.return_value = self.token.expire - timedelta(
            minutes=1
        )
        resp = Client().get(path)
        self.user = models.UserProxy.objects.get(id=self.user.id)
        self.assertIn('alerts', resp.context)
        self.assertEqual(
            'success',
            resp.context['alerts'][0]['type'],
            resp.context['alerts'][0]['text'],
        )
        self.assertTrue(self.user.is_active)

    def test_env_activation_users(self):
        path = reverse('authorisation:signup')
        client = Client()
        with override_settings(NEW_USERS_ACTIVATED=False):
            client.post(
                path,
                data={
                    'username': 'fake_username',
                    'password1': 'fake_password',
                    'password2': 'fake_password',
                    'email': 'email@yandex.ru',
                },
            )
            user = models.UserProxy.inactive.get(username='fake_username')
            self.assertTrue(not user.is_active)
        with override_settings(NEW_USERS_ACTIVATED=True):
            resp = client.post(
                path,
                data={
                    'username': 'fake_username1',
                    'password1': 'fake_password1',
                    'password2': 'fake_password1',
                    'email': 'love_danila_eremin@seniorgoogle.com',
                },
            )
            self.assertRedirects(resp, reverse('authorisation:signup_done'))
            user = models.UserProxy.objects.get(username='fake_username1')
            self.assertTrue(user.is_active)

    def test_unique_email_signup(self):
        form_data = {
            'username': 'some_interesting_username',
            'password1': 'somehotpassword',
            'password2': 'somehotpassword',
            'email': self.user.email,
        }
        form = forms.SignUpForm(form_data)
        form.full_clean()
        self.assertNotIn('email', form.cleaned_data.keys())
        self.assertEqual(1, len(form.errors))


class LoginTests(TestCase):
    def setUp(self) -> None:
        self.user = models.UserProxy.objects.create(
            username='some_test_username_qwerty',
            password=make_password('empty_password'),
            email='danila_eremin_love@google.comtest',
            is_active=True,
        )
        self.user_password = 'empty_password'

    def test_login(self):
        path = reverse('authorisation:login')
        resp = self.client.get(path)
        self.assertEqual(resp.status_code, 200)

    def test_login_by_username(self):
        path = reverse('authorisation:login')
        data = {'username': self.user.username, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertEqual(response.status_code, 302)

    def test_login_by_email(self):
        path = reverse('authorisation:login')
        data = {'username': self.user.email, 'password': self.user_password}
        response = self.client.post(path, data=data)
        self.assertEqual(response.status_code, 302)

    @override_settings(FAILED_AUTHS_TO_DEACTIVATE=5)
    def test_suspicious_activity_on_account_deactivate(self):
        path = reverse('authorisation:login')
        data = {
            'username': self.user.username,
            'password': 'incorrect_password',
        }
        for _ in range(4):
            self.client.post(path, data=data)
            user = models.UserProxy.objects.get(username=self.user.username)
            self.assertTrue(user.is_active)
        self.client.post(path, data=data)
        user = models.UserProxy.inactive.get(username=self.user.username)
        self.assertTrue(not user.is_active)


class UserChangeTests(TestCase):
    def setUp(self) -> None:
        self.user = models.UserProxy.objects.create(
            username='some_test_username_qwerty',
            password=make_password('empty_password'),
            email='danila_eremin_love@google.comtest',
            is_active=True,
        )
        self.user_password = 'empty_password'

    @parameterized.expand(
        (
            ('danila.eremin@ya.ru', 'danila-eremin@yandex.ru'),
            ('danila.eremin@gmail.com', 'danilaeremin@gmail.com'),
            ('d.a.n.i.l.a.l.o.v.e@ya.ru', 'd-a-n-i-l-a-l-o-v-e@yandex.ru'),
            ('d.a.n.i.l.a.l.o.v.e@gmail.com', 'danilalove@gmail.com'),
        )
    )
    def test_email_normalizer(self, test_email, ans_email):
        self.user.email = test_email
        self.user.save()
        self.assertEqual(self.user.profile.normalized_email, ans_email)
