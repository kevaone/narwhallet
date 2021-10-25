import json


class MNarwhalletWebSettings():
    def __init__(self):
        self._sync: dict = None
        self._theme: str = None
        self._ip: str = None
        self._port: int = None
        self._ssl: bool = None
        self._ssl_key: str = None
        self._ssl_cert: str = None

    @property
    def sync(self) -> dict:
        return self._sync

    @property
    def theme(self) -> str:
        return self._theme

    @property
    def ip(self) -> str:
        return self._ip

    @property
    def port(self) -> int:
        return self._port

    @property
    def ssl(self) -> bool:
        return self._ssl

    @property
    def ssl_key(self) -> str:
        return self._ssl_key

    @property
    def ssl_cert(self) -> str:
        return self._ssl_cert

    def set_sync(self, sync: dict):
        self._sync = sync

    def set_theme(self, theme: str):
        self._theme = theme

    def set_ip(self, ip: str):
        # TODO Validate IP formats
        self._ip = ip

    def set_port(self, port: int):
        self._port = port

    def set_ssl(self, ssl: bool):
        self._ssl = ssl

    def set_ssl_key(self, ssl_key: str):
        self._ssl_key = ssl_key

    def set_ssl_cert(self, ssl_cert: str):
        self._ssl_cert = ssl_cert

    def load(self, strap_file: str):
        with open(strap_file, mode='r') as _content_file:
            _data = json.loads(_content_file.read())

        self.fromDict(_data)

    def fromDict(self, _d: dict):
        self.set_sync(_d['sync'])
        self.set_theme(_d['theme'])
        self.set_ip(_d['ip'])
        self.set_port(_d['port'])
        self.set_ssl(_d['ssl'])
        self.set_ssl_key(_d['ssl_key'])
        self.set_ssl_cert(_d['ssl_cert'])

    def toDict(self) -> dict:
        _d = {}
        _d['sync'] = self.sync
        _d['theme'] = self.theme
        _d['ip'] = self.ip
        _d['port'] = self.port
        _d['ssl'] = self.ssl
        _d['ssl_key'] = self.ssl_key
        _d['ssl_cert'] = self.ssl_cert

        return _d
