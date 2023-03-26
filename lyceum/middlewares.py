"""There is a self written middlewares for the project"""
import re
from typing import Any, List, Union

from django.conf import settings
from django.db.models import QuerySet
from django.shortcuts import HttpResponse


class CoffeeTime:
    """middleware that reverses russian words every 10 times"""

    times_to_on = settings.REVERSER_MIDDLEWARE_ENABLE

    _times: int = 0

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

    @staticmethod
    def reverse_words(content_data: bytes) -> bytes:
        """reverses all russian words"""
        content: str = content_data.decode()
        pattern_word = re.compile(r'\b[а-яА-ЯёЁ]*\b')
        pattern_ru_word = re.compile(r'[а-яА-ЯёЁ]+')
        iterator = re.finditer(pattern_word, content)
        raw_new_content: list[str] = []
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


class GroupOptimizedRequestData:
    """
    middleware that grouping many to many fields in optimized requests

    like tags__name in item optimized request
    """

    def __init__(self, get_response: Any) -> None:
        """init class"""
        self.__get_response = get_response
        self.qs: QuerySet[Any] = QuerySet()  # type: ignore[type-arg]

    def __call__(self, request: Any, **kwargs: Any) -> HttpResponse:
        """
        checks every request on containint some models optimized data
        and grouping that by known fields
        """
        response: HttpResponse = self.__get_response(request)
        return response

    def process_template_response(self, request: Any, response: Any) -> Any:
        context = response.resolve_context(response.context_data)
        if 'items' in context:
            self.qs = context['items']
            grouped_item = self.group_items(
                field_name='tags__name', pk='id', is_one=False
            )
            response.context_data['items'] = grouped_item
        if 'item' in context:
            self.qs = context['item']
            grouped_item = self.group_items(
                field_name='tags__name', pk='id', is_one=True
            )
            response.context_data['item'] = grouped_item
        return response

    def group_items(
        self, field_name: str, pk: str, is_one: Any = False
    ) -> Union[List[Any], Any]:
        jindex = 0
        index = 0
        grouped = []
        if self.qs.count():
            grouped.append(self.qs[0])
            grouped[jindex][field_name] = [
                grouped[jindex][field_name],
            ]
            jindex += 1
            while index < self.qs.count() - 1:
                if self.qs[index][pk] != self.qs[index + 1][pk]:
                    grouped.append(self.qs[index + 1])
                    grouped[jindex][field_name] = [
                        self.qs[index + 1][field_name],
                    ]
                    jindex += 1
                else:
                    grouped[jindex - 1][field_name].append(
                        self.qs[index + 1][field_name]
                    )
                index += 1
        if is_one:
            return grouped[0]
        return grouped
