from typing import Dict, List
from narwhallet.core.kcl.wallet.address import MAddress


class MAddresses():
    def __init__(self):
        self._addresses: List[MAddress] = []
        self._names: Dict[str, int] = {}

    @property
    def addresses(self) -> List[MAddress]:
        return self._addresses

    @property
    def count(self) -> int:
        return len(self.addresses)

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

    def from_json(self, address: dict):
        _address = MAddress()

        _address.set_address(address['address'])
        _address.set_sent(address['sent'])
        _address.set_received(address['received'])
        _address.set_balance(address['balance'])
        if 'unconfirmed_receive_balance' in address:
            _address.set_unconfirmed_receive_balance(address['unconfirmed_receive_balance'])
        if 'unconfirmed_send_balance' in address:
            _address.set_unconfirmed_send_balance(address['unconfirmed_send_balance'])
        _address.set_label(address['label'])
        if 'history' in address:
            _address.set_history(address['history'])
        if 'namespaces' in address:
            _address.set_namespaces(address['namespaces'])
        if 'is_multi_sig' in address:
            _address.set_is_multi_sig(address['is_multi_sig'])
        if 'multi_sig_redeem_script' in address:
            _address.set_multi_sig_redeem_script(address['multi_sig_redeem_script'])
        if 'multi_sig_address_indexes' in address:
            _address.set_multi_sig_address_indexes(address['multi_sig_address_indexes'])

        self._addresses.append(_address)
        self._names[_address.address] = len(self._addresses) - 1

    def from_pool(self, address: str, label: str = ''):
        _address = MAddress()

        _address.set_address(address)
        if label != '':
            _address.set_label(label)

        self._addresses.append(_address)
        self._names[_address.address] = len(self._addresses) - 1

    def to_list(self) -> list:
        _l = []
        for i in self.addresses:
            _l.append(i.to_list())
        return _l

    def to_dict_list(self) -> List[dict]:
        _l = []
        for i in self.addresses:
            _l.append(i.to_dict())
        return _l
