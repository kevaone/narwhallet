from core.kcl.models._base import MBase
from core.kcl.models.namespace_keys import MNSKeys


class MNamespace(MBase):
    def __init__(self):
        self._date: int = None
        self._address: str = None
        self._namespaceid: str = None
        self._shortcode: int = 0
        self._keys: MNSKeys = MNSKeys()
        self._wallet: str = None

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

    def toList(self) -> list:
        return [self.date, self.namespaceid, self.shortcode,
                self.wallet, self.keys.toList(), self.address]

    def toDict(self) -> dict:
        return {'date': self.date, 'namespaceid': self.namespaceid,
                'shortcode': self.shortcode, 'wallet': self.wallet,
                'keys': self.keys.toDictList(), 'address': self.address,
                'key_count': self.keys.count}
