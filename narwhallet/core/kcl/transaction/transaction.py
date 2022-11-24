import time
from typing import List
from narwhallet.core.kcl.transaction.input import MTransactionInput
from narwhallet.core.kcl.transaction.output import MTransactionOutput


class MTransaction():
    def __init__(self):
        self._txid: str = ''
        self._hash: str = ''
        self._version: int = -1
        self._size: int = -1
        self._vsize: int = -1
        self._locktime: int = -1
        self._blockhash: str = ''
        self._vin: List[MTransactionInput] = []
        self._vout: List[MTransactionOutput] = []
        self._hex: str = ''
        self._confirmations: int = -1
        self._time: int = -1
        self._blocktime: int = -1

    @property
    def txid(self) -> str:
        return self._txid

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def version(self) -> int:
        return self._version

    @property
    def size(self) -> int:
        return self._size

    @property
    def vsize(self) -> int:
        return self._vsize

    @property
    def locktime(self) -> int:
        return self._locktime

    @property
    def blockhash(self) -> str:
        return self._blockhash

    @property
    def confirmations(self) -> int:
        return self._confirmations

    @property
    def time(self) -> int:
        return self._time

    @property
    def blocktime(self) -> int:
        return self._blocktime

    @property
    def vin(self) -> List[MTransactionInput]:
        return self._vin

    @property
    def vout(self) -> List[MTransactionOutput]:
        return self._vout

    @property
    def hex(self) -> str:
        return self._hex

    def set_txid(self, txid: str) -> None:
        self._txid = txid

    def set_hash(self, thash: str) -> None:
        self._hash = thash

    def set_version(self, version) -> None:
        self._version = version

    def set_size(self, size) -> None:
        self._size = size

    def set_vsize(self, vsize) -> None:
        self._vsize = vsize

    def set_locktime(self, locktime) -> None:
        self._locktime = locktime

    def set_blockhash(self, blockhash: str) -> None:
        self._blockhash = blockhash

    def set_confirmations(self, confirmations) -> None:
        self._confirmations = confirmations

    def set_time(self, time) -> None:
        self._time = time

    def set_blocktime(self, blocktime) -> None:
        self._blocktime = blocktime

    def set_vin(self, vin: List[MTransactionInput]) -> None:
        self._vin = vin

    def set_vout(self, vout: List[MTransactionOutput]) -> None:
        self._vout = vout

    def add_vin(self, vin: MTransactionInput) -> None:
        self._vin.append(vin)

    def add_vout(self, vout: MTransactionOutput) -> None:
        self._vout.append(vout)

    def set_hex(self, thex: str) -> None:
        self._hex = thex

    @staticmethod
    def to_dict_list(v: list) -> List[dict]:
        _l = []
        for i in v:
            if isinstance(i, (MTransactionInput, MTransactionOutput)):
                _l.append(i.to_dict())

        return _l

    def from_sql(self, tx, vin, vout):
        if len(tx) > 0:
            _tx = tx[0]
            self.set_txid(_tx[0])
            self.set_hash(_tx[1])
            self.set_version(_tx[2])
            self.set_size(_tx[3])
            self.set_vsize(_tx[4])
            self.set_locktime(_tx[5])
            self.set_blockhash(_tx[8])
            self.set_confirmations(_tx[9])
            self.set_time(_tx[10])
            self.set_blocktime(_tx[11])
            self.set_hex(_tx[12])

            for i in vin:
                _in = MTransactionInput()
                _in.from_sql(i)
                self.add_vin(_in)

            for i in vout:
                _out = MTransactionOutput()
                _out.from_sql(i)
                self.add_vout(_out)

    def from_json(self, json: dict):
        self.set_txid(json['txid'])
        if 'hash' in json:
            self.set_hash(json['hash'])
        if 'version' in json:
            self.set_version(json['version'])
        if 'size' in json:
            self.set_size(json['size'])
        if 'vsize' in json:
            self.set_vsize(json['vsize'])
        if 'locktime' in json:
            self.set_locktime(json['locktime'])

        for i in json['vin']:
            _in = MTransactionInput()
            _in.from_json(i)
            self.add_vin(_in)

        for i in json['vout']:
            _out = MTransactionOutput()
            _out.from_json(i)
            self.add_vout(_out)

        if 'hex' in json:
            self.set_hex(json['hex'])

        if 'blockhash' in json:
            self.set_blockhash(json['blockhash'])

        if 'confirmations' in json:
            self.set_confirmations(json['confirmations'])

        if 'time' in json:
            self.set_time(json['time'])
        else:
            self.set_time(time.time())

        if 'blocktime' in json:
            self.set_blocktime(json['blocktime'])

    def to_dict(self) -> dict:
        return {'hash': self.hash, 'blockhash': self.blockhash,
                'vin': self.to_dict_list(self.vin),
                'vout': self.to_dict_list(self.vout), 'txid': self.txid,
                'hex': self.hex, 'version': self.version, 'size': self.size,
                'vsize': self.vsize, 'locktime': self.locktime,
                'confirmations': self.confirmations, 'time': self.time,
                'blocktime': self.blocktime}
