from narwhallet.core.kcl.kevacoin.namespace_keys import MNSKeys


class MNamespace():
    def __init__(self):
        self._date: int = -1
        self._address: str = ''
        self._namespaceid: str = ''
        self._shortcode: int = 0
        self._keys: MNSKeys = MNSKeys()
        self._wallet: str = ''

    @property
    def date(self) -> int:
        return self._date

    @property
    def address(self) -> str:
        return self._address

    @property
    def namespaceid(self) -> str:
        return self._namespaceid

    @property
    def shortcode(self) -> float:
        return self._shortcode

    @property
    def keys(self) -> MNSKeys:
        return self._keys

    @property
    def wallet(self) -> str:
        return self._wallet

    def set_date(self, date: int) -> None:
        self._date = date

    def set_address(self, address: str) -> None:
        self._address = address

    def set_namespaceid(self, namespaceid: str) -> None:
        self._namespaceid = namespaceid

    def set_shortcode(self, shortcode: int) -> None:
        self._shortcode = shortcode

    def set_wallet(self, wallet: str) -> None:
        self._wallet = wallet

    def to_list(self) -> list:
        return [self.date, self.namespaceid, self.shortcode,
                self.wallet, self.keys.to_list(), self.address]

    def to_dict(self) -> dict:
        return {'date': self.date, 'namespaceid': self.namespaceid,
                'shortcode': self.shortcode, 'wallet': self.wallet,
                'keys': self.keys.to_dict_list(), 'address': self.address,
                'key_count': self.keys.count}
