"""There is a self written middlewares for the project"""
import re
from typing import Any

from django.shortcuts import HttpResponse


class CoffeeTime:
    """middleware that reverses russian words every 10 times"""

    alphabet: str = (
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    )

    __times: int = 0

    enable = 10

    @staticmethod
    def reverse_words(content_data: bytes) -> bytes:
        """reverses all russian words"""
        content: str = content_data.decode()
        cont: str = ''
        pattern = r'\b[а-яА-ЯёЁ]*\b'
        iterator = re.finditer(pattern, content)
        start: int = 0
        end: int = len(content)
        for word in iterator:
            cont += content[start: word.start(0)]
            cont += word.group(0)[::-1]
            start = word.end(0)
        cont += content[start:end]
        return cont.encode()

    def __init__(self, get_response: Any) -> None:
        """init class"""
        self.__get_response = get_response

    def __call__(self, request: Any) -> HttpResponse:
        """checks every request

        reverses all russian words every 10 request
        """
        response: HttpResponse = self.__get_response(request)
        if self.enable == 0 or (
            self.__times % self.enable == 0 and self.__times != 0
        ):
            response.content = self.reverse_words(response.content)
            self.__times = 0
        self.__times += 1
        return response
