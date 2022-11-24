from typing import Dict, List
from narwhallet.core.kcl.addr_book import MBookAddress
from narwhallet.core.kcl.file_utils.io import AddressBookLoader


class MBookAddresses():
    def __init__(self):
        self.root_path: str = ''
        self._addresses: Dict[str, MBookAddress] = {}

    @property
    def addresses(self) -> Dict[str, MBookAddress]:
        return self._addresses

    @property
    def count(self) -> int:
        return len(self.addresses)

    def get_address_by_name(self, name: str) -> MBookAddress:
        return self._addresses[name]

    def remove_address(self, address: str) -> bool:
        if address in self.addresses:
            del self._addresses[address]
            _return = True
        else:
            _return = False
        return _return

    def from_json(self, address: dict):
        _address = MBookAddress()

        _address.set_coin(address['coin'])
        _address.set_name(address['name'])
        _address.set_address(address['address'])
        _address.set_sent(address['sent'])
        _address.set_received(address['received'])
        _address.set_label(address['label'])

        self._addresses[_address.address] = _address

    def to_list(self) -> list:
        _l = []
        for i in self.addresses:
            _l.append(self.addresses[i].to_list())
        return _l

    def to_dict_list(self) -> List[dict]:
        _l = []
        for i in self.addresses:
            _l.append(self.addresses[i].to_dict())
        return _l

    def save_address_book(self):
        return AddressBookLoader.save(self.root_path, self.to_dict_list())

    def load_address_book(self, path: str):
        self.root_path = path
        _data = AddressBookLoader.load(path)

        for _a in _data:
            self.from_json(_a)
