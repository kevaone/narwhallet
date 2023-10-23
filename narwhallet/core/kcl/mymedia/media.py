class MMedia():
    def __init__(self):
        self._name: str = ''
        self._cid: str = ''
        self._pin_date: str = ''
        self._pin_status: bool = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def cid(self) -> str:
        return self._cid

    @property
    def pin_date(self) -> str:
        return self._pin_date

    @property
    def pin_status(self) -> bool:
        return self._pin_status

    def set_name(self, name: str) -> None:
        self._name = name

    def set_cid(self, cid: str) -> None:
        self._cid = cid

    def set_pin_date(self, date: str) -> None:
        self._pin_date = date

    def set_pin_status(self, status: bool) -> None:
        self._pin_satus = status

    def to_list(self) -> list:
        return [self.name, self.cid, self.pin_date,
                self.pin_status]

    def to_dict(self) -> dict:
        return {'name': self.name, 'cid': self.cid,
                'pin_date': self.pin_date, 'pin_status': self.pin_status}
