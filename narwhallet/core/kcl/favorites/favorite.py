class MFavorite():
    def __init__(self):
        self._id: str = ''
        self._coin: str = ''
        self._kind: str = ''
        self._value: str | list = ''
        self._filter: list = []

    @property
    def id(self) -> str:
        return self._id

    @property
    def coin(self) -> str:
        return self._coin

    @property
    def kind(self) -> str:
        return self._kind

    @property
    def value(self) -> str | list:
        return self._value

    @property
    def filter(self) -> list:
        return self._filter

    def set_coin(self, coin: str) -> None:
        self._coin = coin

    def set_id(self, id: str) -> None:
        self._id = id

    def set_kind(self, kind: str) -> None:
        self._kind = kind

    def set_value(self, value: str | list) -> None:
        self._value = value

    def set_filter(self, filter: list) -> None:
        self._filter = filter

    def to_list(self) -> list:
        return [self.id, self.coin, self.kind, self.value,
                self.filter]

    def to_dict(self) -> dict:
        return {'id': self.id, 'coin': self.coin, 'kind': self.kind,
                'value': self.value, 'filter': self.filter}
