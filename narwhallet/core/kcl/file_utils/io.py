import os
import json
from typing import List
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


class _loader():
    @staticmethod
    def generate_host_key(path):
        _key = AESGCM.generate_key(256)
        file_path = os.path.join('host_key', path)
        with open(file_path, mode='wb') as _file:
            _file.write(_key)
        return True

    @staticmethod
    def _save(file_path: str, data, k=None):
        if isinstance(data, str):
            data = data.encode()

        if k is not None:
            _nonce = os.urandom(12)  # GCM mode needs 12 fresh bytes every time
            data = _nonce + AESGCM(k).encrypt(_nonce, data, b'')
            data = b'narw'+data
        print('file_path', file_path)
        with open(file_path, mode='wb') as _file:
            _file.write(data)
        return True

    @staticmethod
    def _load(file_path: str, k=None):
        with open(file_path, mode='rb') as _file:
            _data = _file.read()
        if k is not None:
            _data = _data[4:]
            try:
                _data = AESGCM(k).decrypt(_data[:12], _data[12:], b'')
            except InvalidTag:
                _data = b'InvalidTag'
        return _data


class ConfigLoader(_loader):
    def __init__(self, config_file: str):
        self.config_file = config_file

    def save(self, data):
        return self._save(self.config_file, data)

    def load(self):
        self.data = json.loads(self._load(self.config_file))
        return True


class WalletLoader(_loader):
    def __init__(self, wallet_path: str, wallet_name: str):
        self.wallet_path = wallet_path
        self.wallet_name = wallet_name
        self.path = os.path.join(self.wallet_path, self.wallet_name)

    def save(self, data, k=None):
        return self._save(self.path, data, k)

    def load(self, k=None):
        return self._load(self.path, k)


class AddressBookLoader(_loader):
    @staticmethod
    def save(root_path: str, data: List[dict]):
        _path = os.path.join(root_path, 'narwhallet.addressbook')
        _loader._save(_path, json.dumps(data, indent=4).encode())
        return True

    @staticmethod
    def load(root_path: str):
        _path = os.path.join(root_path, 'narwhallet.addressbook')
        return json.loads(_loader._load(_path))

class FavoritesLoader(_loader):
    @staticmethod
    def save(root_path: str, data: List[dict]):
        _path = os.path.join(root_path, 'narwhallet.favorites')
        _loader._save(_path, json.dumps(data, indent=4).encode())
        return True

    @staticmethod
    def load(root_path: str):
        _path = os.path.join(root_path, 'narwhallet.favorites')
        return json.loads(_loader._load(_path))


class TransactionLoader(_loader):
    @staticmethod
    def save(root_path: str, data: str):
        _path = os.path.join(root_path, 'tx.cache')
        _loader._save(_path, json.dumps(data, indent=4).encode())
        # _loader._save(_path, json.dumps(data).encode())
        return True

    @staticmethod
    def load(root_path: str):
        _path = os.path.join(root_path, 'tx.cache')
        return json.loads(_loader._load(_path))


class NamespaceLoader(_loader):
    @staticmethod
    def save(root_path: str, data: str):
        _path = os.path.join(root_path, 'ns.cache')
        _loader._save(_path, json.dumps(data, indent=4).encode())
        # _loader._save(_path, json.dumps(data).encode())
        return True

    @staticmethod
    def load(root_path: str):
        _path = os.path.join(root_path, 'ns.cache')
        return json.loads(_loader._load(_path))
