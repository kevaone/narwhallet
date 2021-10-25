from typing import Dict, List
from core.kcl.models.address import MAddress


class MAddresses():
    def __init__(self):
        self._addresses: List[MAddress] = []
        self._names: Dict[int] = {}

    @property
    def addresses(self) -> List[MAddress]:
        return self._addresses

    @property
    def count(self) -> int:
        return len(self.addresses)

    # def add_address(self, address):
    #     # TODO: Type test to select appropriate method
    #     self._fromJson()

    def get_address_by_index(self, index: int) -> MAddress:
        return self._addresses[index]

    def get_address_by_name(self, address: str) -> MAddress:
        return self._addresses[self._names[address]]

    def get_address_index_by_name(self, address: str) -> int:
        if address in self._names:
            _return = self._names[address]
        else:
            _return = -1
        return _return

    def _fromJson(self, address: dict):
        _address = MAddress()

        _address.set_address(address['address'])
        _address.set_sent(address['sent'])
        _address.set_received(address['received'])
        _address.set_balance(address['balance'])
        if 'unconfirmed_balance' in address:
            _address.set_unconfirmed_balance(address['unconfirmed_balance'])
        _address.set_label(address['label'])
        if 'history' in address:
            _address.set_history(address['history'])
        if 'unspent_tx' in address:
            _address.set_unspent_tx(address['unspent_tx'])

        self._addresses.append(_address)
        self._names[_address.address] = len(self._addresses) - 1

    def _fromPool(self, address: str, label: str = None):
        _address = MAddress()

        _address.set_address(address)
        if label is not None:
            _address.set_label(label)

        self._addresses.append(_address)
        self._names[_address.address] = len(self._addresses) - 1

    def toList(self) -> list:
        _l = []
        for i in self.addresses:
            _l.append(i.toList())
        return _l

    def toDictList(self) -> List[dict]:
        _l = []
        for i in self.addresses:
            _l.append(i.toDict())
        return _l
