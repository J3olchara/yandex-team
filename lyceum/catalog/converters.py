class NaturalNumber:
    regex = r'[1-9]\d*'

    def to_python(self, value: str):
        return int(value)

    def to_url(self, value: int):
        return str(value)
