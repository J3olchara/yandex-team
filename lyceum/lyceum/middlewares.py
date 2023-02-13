from django.shortcuts import HttpResponse


class CoffeeTime:
    """middleware that reverses russian words every 10 times"""

    __alphabet = (
        'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    )

    times = 0

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request) -> HttpResponse:
        response: HttpResponse = self.get_response(request)
        if self.times % 10 == 0:
            content: str = response.content.decode()
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
            response.content = cont.encode()
            self.times = 0
        self.times += 1
        return response
