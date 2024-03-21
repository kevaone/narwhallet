import json
from narwhallet.core.kcl.transaction.script_pubkey import MScriptPubKey


class MTransactionOutput():
    def __init__(self):
        self._n: int = -1
        self._value: int = -1
        self._scriptPubKey: MScriptPubKey = MScriptPubKey()

    @property
    def n(self) -> int:
        return self._n

    @property
    def value(self) -> int:
        return self._value

    @property
    def scriptPubKey(self) -> MScriptPubKey:
        return self._scriptPubKey

    def set_n(self, n: int) -> None:
        self._n = n

    def set_value(self, value: int) -> None:
        self._value = value

    def set_scriptPubKey(self, scriptPubKey) -> None:
        self._scriptPubKey = scriptPubKey

    def from_sql(self, vout):
        _sc = MScriptPubKey()
        self.set_value(vout[0])
        self.set_n(vout[1])
        _sc.set_asm(vout[2])
        _sc.set_hex(vout[3])
        _sc.set_reqSigs(vout[4])
        _sc.set_type(vout[5])
        if vout[6] != '':
            _sc.set_addresses(json.loads(vout[6]))
        self.set_scriptPubKey(_sc)

    def from_json(self, json: dict):
        if 'n' in json:
            self.set_n(json['n'])
        if 'value' in json:
            self.set_value(json['value'])
        _sc = MScriptPubKey()
        _sc.from_json(json['scriptPubKey'])
        self.set_scriptPubKey(_sc)

    def to_list(self) -> list:
        return [self.n, self.value, self.scriptPubKey.to_list()]

    def to_dict(self) -> dict:
        return {'n': self.n, 'value': self.value,
                'scriptPubKey': self.scriptPubKey.to_dict()}
