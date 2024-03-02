from typing import Dict, List, Optional
from narwhallet.core.ksc.utils import Ut
from narwhallet.core.kcl.kevacoin.namespace_key import MNSKey


class MNSKeys():
    def __init__(self, data):
        self._keys: List[MNSKey] = []
        self._names: Dict[str, int] = {}

        for _key in data:
            self.add_key(_key)

    @property
    def keys(self) -> List[MNSKey]:
        return self._keys

    @property
    def count(self) -> int:
        return len(self.keys)

    @staticmethod
    def sort(item):
        return item[0]

    @staticmethod
    def sort_dict(item):
        return item['timestamp']

    def clear(self) -> None:
        self._keys = []

    def get_key_by_index(self, index: int) -> MNSKey:
        return self.keys[index]

    def get_key_by_name(self, name: str, convert: bool = False) -> Optional[MNSKey]:
        if convert is True:
            _name = self.decode(name)
        else:
            _name = name

        if _name in self._names:
            _return = self.keys[self._names[_name]]
        else:
            _return = None  # MNSKey()
        return _return

    def delete_key_by_name(self, name: str, convert: bool = False) -> bool:
        if convert is True:
            _name = self.decode(name)
        else:
            _name = name

        if _name in self._names:
            del self._keys[self._names[_name]]
            del self._names[_name]
            _return = True
        else:
            _return = False
        return _return

    @staticmethod
    def decode(data):
        # TODO Refine, use of try/except should not be needed.
        try:
            _d2 = Ut.hex_to_bytes(data).decode()
        except Exception:
            try:
                _d2 = Ut.int_to_bytes(int(data), None, 'little').decode()
            except Exception:
                _d2 = data

        return _d2

    def add_key(self, key: dict) -> int:
        _key = MNSKey(key)

        self._keys.append(_key)
        self._names[_key.key] = len(self._keys) - 1

        return len(self._keys)

    def to_list(self, sort_by_date: bool = True) -> list:
        _l = []
        for i in self.keys:
            _l.append(i.to_list())
        if sort_by_date is True:
            _l.sort(reverse=False, key=self.sort)
        return _l

    def to_dict_list(self, sort_by_date: bool = True) -> List[dict]:
        _l = []
        for i in self.keys:
            _l.append(i.to_dict())
        if sort_by_date is True:
            _l.sort(reverse=True, key=self.sort_dict)
        return _l
