"""There is a self written middlewares for the project"""
import re
from typing import Any

from django.conf import settings
from django.shortcuts import HttpResponse


class CoffeeTime:
    """middleware that reverses russian words every 10 times"""

    times_to_on = settings.REVERSER_MIDDLEWARE_ENABLE

    _times: int = 0

    @staticmethod
    def reverse_words(content_data: bytes) -> bytes:
        """reverses all russian words"""
        content: str = content_data.decode()
        pattern_word = re.compile(r'\b[а-яА-ЯёЁ]*\b')
        pattern_ru_word = re.compile(r'[а-яА-ЯёЁ]+')
        iterator = re.finditer(pattern_word, content)
        raw_new_content: list = []
        start: int = 0
        end: int = len(content)
        for word in iterator:
            if re.match(pattern_ru_word, word.group(0)):
                raw_new_content.append(
                    content[start : word.start(0)]
                )  # isort ignore
                raw_new_content.append(word.group(0)[::-1])
                start = word.end(0)
        raw_new_content.append(content[start:end])
        return ''.join(raw_new_content).encode()

    def __init__(self, get_response: Any) -> None:
        """init class"""
        self.__get_response = get_response

    def __call__(self, request: Any) -> HttpResponse:
        """
        checks every request

        reverses all russian words every
        settings.REVERSER_MIDDLEWARE_enable request
        """
        response: HttpResponse = self.__get_response(request)
        if settings.REVERSER_MIDDLEWARE:
            self._times += 1
            if self.times_to_on == 0 or (self._times % self.times_to_on == 0):
                response.content = self.reverse_words(response.content)
                self.__times = 0
        return response
