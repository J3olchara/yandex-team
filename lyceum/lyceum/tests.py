"""MIDDLEWARE tests"""

from django.test import RequestFactory, TestCase

from . import middlewares


class ReverseMiddlewareTests(TestCase):
    """tests reversing middleware"""

    def setUp(self) -> None:
        """add access to factory"""
        self.factory = RequestFactory()

    def test_middleware_reverser(self) -> None:
        """test reversing middleware work"""
        middlewares.CoffeeTime.enable = 0
        tests = [
            ('hello world!', 'hello world!'),
            ('Привет world', 'тевирП world'),
            ('Helпривет мorld', 'Helпривет мorld'),
            ('Привет мир', 'тевирП рим'),
            ('Да', 'аД'),
            ('Привет, друг', 'тевирП, гурд'),
        ]
        for test, ans in tests:
            request = self.client.get(f'/test/?{test=}')
            self.assertIn(ans, request.content.decode())
        middlewares.CoffeeTime.enable = 10
