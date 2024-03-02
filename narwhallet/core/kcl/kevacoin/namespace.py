import json
from narwhallet.core.kcl.kevacoin.namespace_keys import MNSKeys


class MNamespace():
    def __init__(self, ns_data, wallet = None):
        self._address: str = ''
        self._date: str = ''
        self._keys: MNSKeys = MNSKeys(ns_data['data'])
        self._name: str = ''
        self._namespaceid: str = ''
        self._creator: str = ''
        self._shortcode: int = 0
        self._social_name: str = ''
        self._timestamp: int = -1
        self._wallet: str = wallet

        self.set_address()
        self.set_creator()
        self.set_date()
        self.set_name()
        self.set_namespaceid(ns_data['dnsid'])
        self.set_shortcode(ns_data['root_shortcode'])
        self.set_social_name()

    @property
    def address(self) -> str:
        return self._address

    @property
    def creator(self) -> str:
        return self._creator

    @property
    def date(self) -> str:
        return self._date

    @property
    def keys(self) -> MNSKeys:
        return self._keys

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespaceid(self) -> str:
        return self._namespaceid

    @property
    def shortcode(self) -> int:
        return self._shortcode

    @property
    def social_name(self) -> str:
        return self._social_name

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def wallet(self) -> str:
        return self._wallet

    def set_address(self) -> None:
        self._address = self.keys.keys[-1].address

    def set_creator(self) -> None:
        if self.keys.keys[0].op == 'KEVA_NAMESPACE':
            self._creator = self.keys.keys[0].address

    def set_date(self) -> None:
        self._date, self._timestamp = self.keys.keys[0].date

    def set_name(self) -> None:
        for _key in self.keys.keys:
            if _key.dkey == '_KEVA_NS_':
                self._name = _key.dvalue

    def set_namespaceid(self, namespaceid: str) -> None:
        self._namespaceid = namespaceid

    def set_shortcode(self, shortcode: int) -> None:
        self._shortcode = shortcode

    def set_social_name(self) -> None:
        for _key in self.keys.keys:
            if _key.dkey == '\x01_KEVA_NS_':
                self._social_name = json.loads(_key.dvalue)['displayName']

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
