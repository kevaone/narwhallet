

from narwhallet.core.ksc.utils import Ut


class TransactionScriptSigError(Exception):
    pass

class MScriptSig():
    def __init__(self):
        self._asm: str = ''
        self._hex: str = ''
        self._script: bytes = b''

    @property
    def asm(self) -> str:
        return self._asm

    @property
    def hex(self) -> str:
        return self._hex

    @property
    def script(self) -> bytes:
        return self._script

    @property
    def size(self) -> int:
        _size = 0
        # _size = _size + len(Ut.to_cuint(len(self._script)))
        _size = _size + len(self.script)

        return _size

    def set_asm(self, asm: str) -> None:
        self._asm = asm

    def set_hex(self, sighex: str) -> None:
        self._hex = sighex

    def set_script(self, script: bytes | str) -> None:
        if isinstance(script, str):
            try:
                script = Ut.hex_to_bytes(script)
            except Exception as Ex:
                raise TransactionScriptSigError(f'Failed to set transaction scriptsig from hex: {Ex}')

        # TODO: Add script validation

        self._script = script

    def from_json(self, json: dict):
        self.set_asm(json['asm'])
        self.set_hex(json['hex'])

    def to_list(self) -> list:
        return [self.asm, self.hex]

    def to_dict(self) -> dict:
        return {'asm': self.asm, 'hex': self.hex}
