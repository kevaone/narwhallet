from core.kcl.models._base import MBase


class MScriptSig(MBase):
    def __init__(self):
        self._asm: str = None
        self._hex: str = None

    @property
    def asm(self) -> str:
        return self._asm

    @property
    def hex(self) -> str:
        return self._hex

    def set_asm(self, asm: str) -> None:
        self._asm = asm

    def set_hex(self, sighex: str) -> None:
        self._hex = sighex

    def fromJson(self, json: dict):
        self.set_asm(json['asm'])
        self.set_hex(json['hex'])

    def toList(self) -> list:
        return [self.asm, self.hex]

    def toDict(self) -> dict:
        return {'asm': self.asm, 'hex': self.hex}
