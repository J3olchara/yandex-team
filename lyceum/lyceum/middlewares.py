"""There is a self written middlewares for the project"""
from typing import Any

from django.shortcuts import HttpResponse


class CoffeeTime:
    """middleware that reverses russian words every 10 times"""

    __alphabet = (
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    )

    __times = 0

    def reverse_words(self, content: bytes):
        """reverses all russian words"""
        content = content.decode()
        cont: str = ''
        i: int = 0
        while i < len(content):
            while i < len(content) and content[i] not in self.__alphabet:
                cont += content[i]
                i += 1
            tmp = ''
            while i < len(content) and content[i] in self.__alphabet:
                tmp += content[i]
                i += 1
            cont += tmp[::-1]
        self.__times = 0
        return cont.encode()

    def __init__(self, get_response: Any) -> None:
        """init class"""
        self.__get_response = get_response

    def __call__(self, request: Any) -> HttpResponse:
        """checks every request and reversing all"""
        """russian words every 10 request"""
        response: HttpResponse = self.__get_response(request)
        if self.__times % 10 == 0:
            response.content = self.reverse_words(response.content)
        self.__times += 1
        return response
