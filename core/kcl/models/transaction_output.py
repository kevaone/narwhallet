import json
from core.kcl.models._base import MBase
from core.kcl.models.script_pubkey import MScriptPubKey


class MTransactionOutput(MBase):
    def __init__(self):
        self._n: int = None
        self._value: float = None
        self._scriptPubKey: MScriptPubKey = MScriptPubKey()

    @property
    def n(self) -> int:
        return self._n

    @property
    def value(self) -> float:
        return self._value

    @property
    def scriptPubKey(self) -> MScriptPubKey:
        return self._scriptPubKey

    def set_n(self, n: int) -> None:
        self._n = n

    def set_value(self, value: float) -> None:
        self._value = value

    def set_scriptPubKey(self, scriptPubKey) -> None:
        self._scriptPubKey = scriptPubKey

    def fromSQL(self, vout):
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

    def fromJson(self, json: dict):
        if 'n' in json:
            self.set_n(json['n'])
        if 'value' in json:
            self.set_value(json['value'])
        _sc = MScriptPubKey()
        _sc.fromJson(json['scriptPubKey'])
        self.set_scriptPubKey(_sc)

    def toList(self) -> list:
        return [self.n, self.value, self.scriptPubKey.toList()]

    def toDict(self) -> dict:
        return {'n': self.n, 'value': self.value,
                'scriptPubKey': self.scriptPubKey.toDict()}
