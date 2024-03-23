import math
from typing import List
from narwhallet.core.kcl.transaction.input import MTransactionInput
from narwhallet.core.kcl.transaction.output import MTransactionOutput
from narwhallet.core.kcl.transaction.witness import MTransactionWitness
from narwhallet.core.ksc.utils import Ut


class TransactionError(Exception):
    pass

class MTransaction():
    def __init__(self):
        self._blockhash: str = ''
        self._confirmations: int = -1
        self._time: int = -1
        self._blocktime: int = -1

        self._version: bytes = self.set_version(b'\x02\x00\x00\x00')
        self._marker: bytes = self.set_marker(b'\x00')
        self._flag: bytes = self.set_flag(b'\x01')
        self._vin: List[MTransactionInput] = []
        self._vout: List[MTransactionOutput] = []
        self._witnesses: List[MTransactionWitness] = []
        self._locktime: bytes = self.set_locktime(b'\x00\x00\x00\x00')

        self._hex: str = ''
        self._txid: str = ''
        self._hash: str = ''
        self._size: int = -1
        self._vsize: int = -1

    @property
    def txid(self) -> str:
        # TODO: Calculate txid
        return self._txid

    @property
    def hash(self) -> str:
        # TODO: Calculate hash
        return self._hash

    @property
    def version(self) -> bytes:
        return self._version

    @property
    def size(self) -> int:
        return self._size

    @property
    def vsize(self) -> int:
        return self._vsize

    @property
    def locktime(self) -> bytes:
        return self._locktime

    @property
    def marker(self) -> bytes:
        return self._marker

    @property
    def flag(self) -> bytes:
        return self._flag

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
        # TODO: Calculate hex
        return self._hex

    @property
    def witnesses(self) -> list[MTransactionWitness]:
        return self._witnesses

    def add_witness(self, witness_data: bytes | str | list) -> MTransactionWitness:
        _witness = MTransactionWitness()
        _witness.add_stack_item(witness_data)
        
        self.witnesses.append(_witness)
        return _witness

    def set_witnesses(self, witness_data: bytes | str| list) -> None:
        if isinstance(witness_data, str):
            try:
                witness_data = Ut.hex_to_bytes(witness_data)
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction witnesses from hex: {Ex}')
        elif isinstance(witness_data, list):
            try:
                witness_data = witness_data
                # TODO Validate data within list
                return
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction witnesses from list: {Ex}')

        try:
            # TODO Parse witness data
            self.add_witness(b'')
        except Exception as Ex:
            raise TransactionError(f'Failed to set transaction witnesses from bytes: {Ex}')

    def set_version(self, version: bytes | str | int) -> bytes:
        if isinstance(version, str):
            try:
                version = Ut.hex_to_bytes(version)
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction version from hex: {Ex}')
        elif isinstance(version, int):
            try:
                version = Ut.int_to_bytes(version, 4, 'little')
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction version from integer: {Ex}')

        if len(version) != 4:
            raise TransactionError(f'Failed to set transaction version: Version is 4 bytes, {len(version)} bytes supplied.')

        if version not in (b'\x01\x00\x00\x00', b'\x02\x00\x00\x00', b'\x00q\x00\x00'):
            raise TransactionError(f'Failed to set transaction version: Unsupported version, {Ut.bytes_to_hex(version)}.')

        self._version = version
        return self._version

    def _calc_size(self, in_count, out_count) -> None:
        _out_size = 0

        for _out in self.vout:
            _out_size += 1 + 8 + len(_out.scriptpubkey.script)

        if len(self.vout) + 1 == out_count:
            _out_size += 32

        _base = (64 * in_count) + _out_size + 10
        _size = _base + (107 * in_count) + in_count
        _total_size = _size + 2
        _vsize = math.ceil((_base * 3 + _total_size) / 4)

        # TODO: Finish size calculation refinements
        # _input_size = 0
        # _input_size = _input_size + len(self.vin)
        # for _input in self.vin:
        #     _input_size = _input_size + _input.size
        
        # _output_size = 0
        # _output_size = _output_size + len(self.vout)
        # for _output in self.vout:
        #     _output_size = _output_size + _output.size

        # _witness_size = 0
        # for _witness in self.witnesses:
        #     _witness_size = _witness_size + _witness.size

        # _tsize = 0
        # _tsize = _tsize + len(self.version)
        # _tsize = _tsize + len(self.marker)
        # _tsize = _tsize + len(self.flag)
        # _tsize = _tsize + _input_size
        # _tsize = _tsize + _output_size
        # _tsize = _tsize + _witness_size 
        # _tsize = _tsize + len(self.locktime)

        # _wusize = 0
        # _wusize = _wusize + (len(self.version) * 4)
        # _wusize = _wusize + len(self.marker)
        # _wusize = _wusize + len(self.flag)
        # _wusize = _wusize + (_input_size * 4)
        # _wusize = _wusize + (_output_size * 4)
        # _wusize = _wusize + _witness_size 
        # _wusize = _wusize + (len(self.locktime) * 4)

        # n_vsize = 0.0
        # n_vsize = n_vsize + len(self.version)
        # n_vsize = n_vsize + (len(self.marker) * 0.25)
        # n_vsize = n_vsize + (len(self.flag) * 0.25)
        # n_vsize = n_vsize + _input_size 
        # n_vsize = n_vsize + _output_size
        # n_vsize = n_vsize + (_witness_size * 0.25)
        # n_vsize = n_vsize + len(self.locktime)

        self._vsize = _vsize
        self._size = _total_size
        # print('total size', _total_size, 'vsize', _vsize)
        # print('wu size', _wusize, 'new_vsize', n_vsize, '_tsize', _tsize)

    def calc_size(self, in_count, out_count):
        self._calc_size(in_count, out_count)
        return self.size, self.vsize

    def set_locktime(self, locktime: bytes | str | int) -> bytes:
        if isinstance(locktime, str):
            try:
                locktime = Ut.hex_to_bytes(locktime)
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction locktime from hex: {Ex}')
        elif isinstance(locktime, int):
            try:
                locktime = Ut.int_to_bytes(locktime, 4, 'little')
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction locktime from integer: {Ex}')

        if len(locktime) != 4:
            raise TransactionError(f'Failed to set transaction locktime: Locktime is 4 bytes, {len(locktime)} bytes supplied.')

        # if Ut.bytes_to_int(locktime, 'little') < Ut.bytes_to_int(b'\x00\x00\x00\x00', 'little') and Ut.bytes_to_int(locktime, 'little') > Ut.bytes_to_int(b'\xff\xff\xff\xff', 'little'):
        if locktime < b'\x00\x00\x00\x00' and locktime > b'\xff\xff\xff\xff':
            raise TransactionError(f'Failed to set transaction locktime: Unsupported locktime, {Ut.bytes_to_hex(locktime)}.')

        self._locktime = locktime
        return self._locktime

    def set_marker(self, marker: bytes | str | int) -> bytes:
        if isinstance(marker, str):
            try:
                marker = Ut.hex_to_bytes(marker)
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction marker from hex: {Ex}')
        elif isinstance(marker, int):
            try:
                marker = Ut.int_to_bytes(marker, 1, 'little')
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction marker from integer: {Ex}')

        if len(marker) != 1:
            raise TransactionError(f'Failed to set transaction marker: marker is 1 byte, {len(marker)} bytes supplied.')

        if marker != b'\x00':
            raise TransactionError(f'Failed to set transaction marker: Unsupported marker, {Ut.bytes_to_hex(marker)}.')

        self._marker = marker
        return self._marker

    def set_flag(self, flag: bytes | str | int) -> bytes:
        if isinstance(flag, str):
            try:
                flag = Ut.hex_to_bytes(flag)
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction flag from hex: {Ex}')
        elif isinstance(flag, int):
            try:
                flag = Ut.int_to_bytes(flag, 1, 'little')
            except Exception as Ex:
                raise TransactionError(f'Failed to set transaction flag from integer: {Ex}')

        if len(flag) != 1:
            raise TransactionError(f'Failed to set transaction flag: flag is 1 byte, {len(flag)} bytes supplied.')

        if flag == b'\x00':
            raise TransactionError(f'Failed to set transaction flag: Unsupported flag, {Ut.bytes_to_hex(flag)}.')

        self._flag = flag
        return self._flag

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
