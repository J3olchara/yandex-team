"""MIDDLEWARE tests"""
from typing import List

from django.test import RequestFactory, TestCase

from . import middlewares


class ReverseMiddlewareTests(TestCase):
    """tests reversing middleware"""

    def setUp(self) -> None:
        """add access to factory"""
        self.factory = RequestFactory()

    def test_middleware_reverser(self) -> None:
        """test reversing middleware work"""
        contents: List[bytes] = []
        for _ in range(11):
            request = self.client.get('/')
            contents.append(request.content)
        contents_unique = list(set(contents))
        self.assertEqual(len(contents_unique), 2, 'CoffeeTime is not working')
        self.assertEqual(
            contents_unique[0],
            middlewares.CoffeeTime.reverse_words(contents_unique[1]),
            "CoffeeTime doesnt reversing an str"
        )
