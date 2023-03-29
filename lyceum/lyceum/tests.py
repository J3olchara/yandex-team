"""MIDDLEWARE tests"""

from typing import List
from unittest import mock

from django.conf import settings
from django.test import Client, TestCase, modify_settings, override_settings
from django.urls import reverse
from django.utils.timezone import datetime, timedelta
from parameterized import parameterized

import authorisation.models  # noqa: I100
import lyceum.middlewares as lyceum_middlewares  # noqa: I100


@modify_settings(
    MIDDLEWARE={
        'append': 'lyceum.middlewares.CoffeeTime',
        'remove': [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
    }
)
@override_settings(REVERSER_MIDDLEWARE=True)
class ReverseMiddlewareTests(TestCase):
    """tests reversing middleware"""

    @parameterized.expand(  # type: ignore[misc]
        [
            ('hello world!', 'hello world!'),
            ('Привет world', 'тевирП world'),
            ('Helпривет мorld', 'Helпривет мorld'),
            ('Привет мир', 'тевирП рим'),
            ('Да', 'аД'),
            ('Привет, друг', 'тевирП, гурд'),
        ]
    )
    def test_reverser(self, test: str, answer: str) -> None:
        """test reversing function work"""
        content: bytes = lyceum_middlewares.CoffeeTime.reverse_words(
            test.encode()
        )
        self.assertIn(answer, content.decode())

    def test_work(self) -> None:
        """tests middleware working all in all"""
        test_string = 'Привет мир'
        rev_string = 'тевирП рим'
        content: List[str] = []
        for _ in range(lyceum_middlewares.CoffeeTime.times_to_on):
            request = self.client.get(
                reverse('home:test'), data={'test': test_string}
            )
            content.append(request.content.decode())
        self.assertIn(test_string, content)
        self.assertIn(rev_string, content)

    def test_enable_setting(self) -> None:
        """tests correct working of enable setting"""
        test_string = 'Привет мир'
        rev_string = 'тевирП рим'
        contents: List[str] = []
        for _ in range(lyceum_middlewares.CoffeeTime.times_to_on - 1):
            request = self.client.get(
                reverse('home:test'), data={'test': test_string}
            )
            contents.append(request.content.decode())
        self.client.get(reverse('home:test'), data={'test': test_string})
        self.assertEqual(len(set(contents)), 1)
        contents.clear()
        for _ in range(lyceum_middlewares.CoffeeTime.times_to_on * 2 - 1):
            request = self.client.get(
                reverse('home:test'), data={'test': test_string}
            )
            contents.append(request.content.decode())
        self.assertEqual(
            contents.count(test_string),
            lyceum_middlewares.CoffeeTime.times_to_on * 2 - 2,
        )
        self.assertEqual(contents.count(rev_string), 1)

    def test_switcher_environ(self) -> None:
        """tests correct working of switcher"""
        tmp_times_to_on = lyceum_middlewares.CoffeeTime.times_to_on
        lyceum_middlewares.CoffeeTime.times_to_on = 1
        test_string = 'Привет мир'
        rev_string = 'тевирП рим'

        with self.settings(REVERSER_MIDDLEWARE=False):
            request = self.client.get(
                reverse('home:test'), data={'test': test_string}
            )
            self.assertEqual(
                request.content.decode(),
                test_string,
                settings.REVERSER_MIDDLEWARE,
            )

        with self.settings(REVERSER_MIDDLEWARE=True):
            request = self.client.get(
                reverse('home:test'), data={'test': test_string}
            )
            self.assertEqual(
                request.content.decode(),
                rev_string,
                settings.REVERSER_MIDDLEWARE,
            )
        lyceum_middlewares.CoffeeTime.times_to_on = tmp_times_to_on


class TestContextProcessors(TestCase):
    def setUp(self) -> None:
        self.user = authorisation.models.UserProxy.objects.create_user(
            username='some_unique_username',
            email='danilaeremin_test@google.com',
            password='some_super_secret_password',
        )

    @parameterized.expand(
        (
            ['home:home'],
            ['catalog:catalog'],
        )
    )
    @mock.patch('lyceum.context_processors.datetime')
    def test_birthdays_cp(self, template_name, mocked):
        path = reverse(template_name)
        td = timedelta(days=1)
        today = datetime.today()
        self.user.profile.birthday = today
        self.user.profile.save()
        client = Client()

        mocked.today.return_value = today
        resp_good = client.get(path)
        self.assertIn('today_birthdays', resp_good.context.keys())
        self.assertIn(self.user.profile, resp_good.context['today_birthdays'])

        mocked.today.return_value = today - td
        resp_bad = client.get(path)
        self.assertNotIn(
            self.user.profile, resp_bad.context['today_birthdays']
        )

        mocked.today.return_value = today + td
        resp_bad = client.get(path)
        self.assertNotIn(
            self.user.profile, resp_bad.context['today_birthdays']
        )
