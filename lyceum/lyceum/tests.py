"""MIDDLEWARE tests"""

from typing import List

from django.conf import settings
from django.test import TestCase, modify_settings, override_settings
from django.urls import reverse
from parameterized import parameterized

from . import middlewares


@modify_settings(
    MIDDLEWARE={
        'append': 'lyceum.middlewares.CoffeeTime',
        'remove': settings.COMMON_MIDDLEWARES,
    }
)
@override_settings(REVERSER_MIDDLEWARE=True)
class ReverseMiddlewareTests(TestCase):
    """tests reversing middleware"""

    @parameterized.expand([
            ('hello world!', 'hello world!'),
            ('Привет world', 'тевирП world'),
            ('Helпривет мorld', 'Helпривет мorld'),
            ('Привет мир', 'тевирП рим'),
            ('Да', 'аД'),
            ('Привет, друг', 'тевирП, гурд'),
        ])
    def test_reverser(self, test, answer) -> None:
        """test reversing function work"""
        content: bytes = middlewares.CoffeeTime.reverse_words(
            test.encode()
        )
        self.assertIn(answer, content.decode())

    def test_work(self) -> None:
        """tests middleware working all in all"""
        test_string = 'Привет мир'
        rev_string = 'тевирП рим'
        content: List[str] = []
        for _ in range(middlewares.CoffeeTime.times_to_on):
            request = self.client.get(
                reverse('test'), data={'test': test_string}
            )
            content.append(request.content.decode())
        self.assertIn(test_string, content)
        self.assertIn(rev_string, content)

    def test_enable_setting(self) -> None:
        """tests correct working of enable setting"""
        test_string = 'Привет мир'
        rev_string = 'тевирП рим'
        contents: List[str] = []
        for _ in range(middlewares.CoffeeTime.times_to_on - 1):
            request = self.client.get(
                reverse('test'), data={'test': test_string}
            )
            contents.append(request.content.decode())
        self.client.get(reverse('test'), data={'test': test_string})
        self.assertEqual(len(set(contents)), 1)
        contents.clear()
        for _ in range(middlewares.CoffeeTime.times_to_on * 2 - 1):
            request = self.client.get(
                reverse('test'), data={'test': test_string}
            )
            contents.append(request.content.decode())
        self.assertEqual(
            contents.count(test_string),
            middlewares.CoffeeTime.times_to_on * 2 - 2,
        )
        self.assertEqual(contents.count(rev_string), 1)

    def test_switcher_environ(self) -> None:
        """tests correct working of switcher"""
        tmp_times_to_on = middlewares.CoffeeTime.times_to_on
        middlewares.CoffeeTime.times_to_on = 1
        test_string = 'Привет мир'
        rev_string = 'тевирП рим'

        with self.settings(REVERSER_MIDDLEWARE=False):
            request = self.client.get(
                reverse('test'), data={'test': test_string}
            )
            self.assertEqual(
                request.content.decode(),
                test_string,
                settings.REVERSER_MIDDLEWARE,
            )

        with self.settings(REVERSER_MIDDLEWARE=True):
            request = self.client.get(
                reverse('test'), data={'test': test_string}
            )
            self.assertEqual(
                request.content.decode(),
                rev_string,
                settings.REVERSER_MIDDLEWARE,
            )
        middlewares.CoffeeTime.times_to_on = tmp_times_to_on
