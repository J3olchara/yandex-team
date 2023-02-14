"""MIDDLEWARE tests"""
from django.test import RequestFactory, TestCase  # isort:skip

from mock import MagicMock

from . import middlewares


class ReverseMiddlewareTests(TestCase):
    """tests reversing middleware"""

    def setUp(self) -> None:
        """add access to factory"""
        self.factory = RequestFactory()

    def test_middleware_reverser(self) -> None:
        """test reversing middleware work"""
        get_response = MagicMock()
        request = self.factory.get('/')
        middleware = middlewares.CoffeeTime(get_response)
        response = middleware(request)
        self.assertEqual(
            get_response.return_value,
            response,
            'CoffeeTime MIDDLEWARE is not working',
        )
