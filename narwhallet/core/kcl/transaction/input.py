from narwhallet.core.kcl.transaction.script_sig import MScriptSig
from narwhallet.core.ksc.utils import Ut


class TransactionInputError(Exception):
    pass

class MTransactionInput():
    def __init__(self):
        self.tb_address: int = -1
        self.tb_address_chain: int = -1
        self.tb_value: int = -1

        self._txid: bytes = b''
        self._vout: bytes = b''
        self._scriptsig: MScriptSig = MScriptSig()
        self._sequence: bytes = self.set_sequence(b'\xff\xff\xff\xff')

    @property
    def txid(self) -> bytes:
        return self._txid

    @property
    def vout(self) -> bytes:
        return self._vout

    @property
    def scriptsig(self) -> MScriptSig:
        return self._scriptsig

    @property
    def sequence(self) -> bytes:
        return self._sequence

    @property
    def size(self) -> int:
        _size = 0
        _size = _size + len(self.txid)
        _size = _size + len(self.vout)
        _size = _size + self.scriptsig.size
        _size = _size + len(self.sequence)

        return _size

    def set_txid(self, txid: bytes | str) -> None:
        if isinstance(txid, str):
            try:
                txid = Ut.hex_to_bytes(txid)
            except Exception as Ex:
                raise TransactionInputError(f'Failed to set transaction input txid from hex: {Ex}')

        self._txid = txid

    def set_vout(self, vout: bytes | str | int) -> None:
        if isinstance(vout, str):
            try:
                vout = Ut.hex_to_bytes(vout)
            except Exception as Ex:
                raise TransactionInputError(f'Failed to set transaction input vout from hex: {Ex}')
        elif isinstance(vout, int):
            try:
                vout = Ut.int_to_bytes(vout, 4, 'little')
            except Exception as Ex:
                raise TransactionInputError(f'Failed to set transaction input vout from int: {Ex}')

        if len(vout) != 4:
            raise TransactionInputError(f'Failed to set transaction input vout: Input vout is 4 bytes, {len(vout)} bytes supplied.')

        self._vout = vout

    def set_scriptsig(self, script: bytes | str) -> None:
        self.scriptsig.set_script(script)

    def set_sequence(self, sequence: bytes | str) -> bytes:
        if isinstance(sequence, str):
            sequence = Ut.hex_to_bytes(sequence)

        if sequence not in (b'\xff\xff\xff\xff', b'\xfd\xff\xff\xff', b'\xfe\xff\xff\xff'):
            if (sequence < b'\x00\x00@\x00' and sequence > b'\xff\xff@\x00') \
                and (sequence < b'\x00\x00\x00\x00' and sequence > b'\xff\xff\x00\x00'):
                
                raise TransactionInputError(f'Failed to set transaction input sequence: Unsupported unsupported sequence, {Ut.bytes_to_hex(sequence)}.')

        self._sequence = sequence
        return self._sequence
