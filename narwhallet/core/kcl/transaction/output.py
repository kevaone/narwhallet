from narwhallet.core.kcl.transaction.script_pubkey import MScriptPubKey
from narwhallet.core.ksc.utils import Ut


class TransactionOutputError(Exception):
    pass

class MTransactionOutput():
    def __init__(self):
        self._n: int = -1

        self._amount: bytes = b''
        self._scriptpubkey: MScriptPubKey = MScriptPubKey()

    @property
    def n(self) -> int:
        return self._n

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

    def set_n(self, n: int) -> None:
        self._n = n

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

    # def from_sql(self, vout):
    #     _sc = MScriptPubKey()
    #     self.set_value(vout[0])
    #     self.set_n(vout[1])
    #     _sc.set_asm(vout[2])
    #     _sc.set_hex(vout[3])
    #     _sc.set_reqSigs(vout[4])
    #     _sc.set_type(vout[5])
    #     if vout[6] != '':
    #         _sc.set_addresses(json.loads(vout[6]))
    #     self.set_scriptPubKey(_sc)

    # def from_json(self, json: dict):
    #     if 'n' in json:
    #         self.set_n(json['n'])
    #     if 'value' in json:
    #         self.set_value(json['value'])
    #     _sc = MScriptPubKey()
    #     _sc.from_json(json['scriptPubKey'])
    #     self.set_scriptPubKey(_sc)

    # def to_list(self) -> list:
    #     return [self.n, self.value, self.scriptPubKey.to_list()]

    # def to_dict(self) -> dict:
    #     return {'n': self.n, 'value': self.value,
    #             'scriptPubKey': self.scriptPubKey.to_dict()}
