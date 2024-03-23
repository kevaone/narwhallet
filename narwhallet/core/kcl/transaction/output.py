from narwhallet.core.kcl.transaction.script_pubkey import MScriptPubKey
from narwhallet.core.ksc.utils import Ut


class TransactionOutputError(Exception):
    pass

class MTransactionOutput():
    def __init__(self):
        self._amount: bytes = b''
        self._scriptpubkey: MScriptPubKey = MScriptPubKey()

    @property
    def amount(self) -> bytes:
        return self._amount

    @property
    def scriptpubkey(self) -> MScriptPubKey:
        return self._scriptpubkey

    @property
    def size(self) -> int:
        _size = 0
        _size = _size + len(self.amount)
        _size = _size + self.scriptpubkey.size

        return _size

    def set_amount(self, amount: bytes | str | int | float) -> None:
        if isinstance(amount, str):
            try:
                amount = Ut.hex_to_bytes(amount)
            except Exception as Ex:
                raise TransactionOutputError(f'Failed to set transaction output amount from hex: {Ex}')
        elif isinstance(amount, int):
            try:
                amount = Ut.int_to_bytes(amount, 8, 'little')
            except Exception as Ex:
                raise TransactionOutputError(f'Failed to set transaction output amount from int: {Ex}')
        elif isinstance(amount, float):
            try:
                amount = Ut.to_sats(amount)
                amount = Ut.int_to_bytes(amount, 8, 'little')
            except Exception as Ex:
                raise TransactionOutputError(f'Failed to set transaction output amount from float: {Ex}')

        if len(amount) != 8:
            raise TransactionOutputError(f'Failed to set transaction output amount: Output amount is 8 bytes, {len(amount)} bytes supplied.')
     
        self._amount = amount

    def set_scriptpubkey(self, scriptpubkey) -> None:
        self.scriptpubkey.set_script(scriptpubkey)
