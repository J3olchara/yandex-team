"""
Converters module for Feedback

write your converter classes here
"""


class BooleanConverter:
    """boolean path converter"""

    regex = r'[0-1]'

    def to_python(self, value: str) -> bool:
        """convert to value for the function"""
        return bool(int(value))

    def to_url(self, value: bool) -> str:
        """converting to value for the path"""
        return str(int(value))
