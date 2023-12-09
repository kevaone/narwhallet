import json
import time
from typing import List
from narwhallet.core.kex.peer import Peer
from narwhallet.core.kex.api import _api
from narwhallet.core.kex.cmd_base import _cmd


class KEXclient():
    def __init__(self):
        self.api: _api = _api()
        self.peers: List[Peer] = []
        self.active_peer: int = -1
        self.id: int = 0

    def add_peer(self, host: str, port: int, tls: bool, validate_cert: bool):
        peer = Peer(host, port, tls, validate_cert)
        self.peers.append(peer)
        return len(self.peers)-1

    def call(self, command: _cmd):
        try:
            while self.peers[self.active_peer].busy is True:
                # print('peer busy, retry in 1 seconds...')
                time.sleep(1)
            data = self.peers[self.active_peer].comm(command)
            self.id += 1
        except Exception:
            data = b''

        try:
            _ = json.loads(data.decode())
        except Exception:
            data = b''

        return data.decode()

    def call_batch(self, commands: list, json_test: bool = True):
        try:
            while self.peers[self.active_peer].busy is True:
                # print('peer busy, sleeping 1sec...')
                time.sleep(1)
            data = self.peers[self.active_peer].comm(commands)
        except Exception:
            data = b'[]'

        try:
            if json_test is True:
                _ = json.loads(data.decode())
        except Exception:
            data = b'[]'

        return data.decode()
