

class MNSKey():
    def __init__(self):
        self._date: int = None
        self._key: str = None
        self._value: str = None

    @property
    def date(self) -> int:
        return self._date

    @property
    def key(self) -> str:
        return self._key

    @property
    def value(self) -> str:
        return self._value

    def set_date(self, date: int) -> None:
        self._date = date

    def set_key(self, key: str) -> None:
        self._key = key

    def set_value(self, value: str) -> None:
        self._value = value

    def to_list(self) -> list:
        return [self.date, self.key, self.value]

    def to_dict(self) -> dict:
        return {'date': self.date, 'key': self.key, 'value': self.value}
