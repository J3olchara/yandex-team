from django.shortcuts import HttpResponse

from . import settings


class CoffeeTime:

    __alphabet = (
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: HttpResponse = self.get_response(request)
        content = response.content.decode()
        cont = ''
        i = 0
        while i < len(content):
            while i < len(content) and content[i] not in self.__alphabet:
                cont += content[i]
                i += 1
            tmp = ''
            while i < len(content) and content[i] in self.__alphabet:
                tmp += content[i]
                i += 1
            cont += tmp[::-1]
        response.content = cont.encode()
        return response
