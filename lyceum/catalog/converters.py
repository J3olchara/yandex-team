"""Converters module for project"""
import re


class NaturalNumber:
    """natural number converter"""

    regex = r'[1-9]\d*'

    def to_python(self, value: str) -> int:
        """convert to value for the function"""
        return int(value)

    def to_url(self, value: int) -> str:
        """converting to value for the path"""
        return str(value)
