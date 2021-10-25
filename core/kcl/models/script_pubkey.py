from typing import List
from core.kcl.models._base import MBase


class MScriptPubKey(MBase):
    def __init__(self):
        self._asm: str = None
        self._hex: str = None
        self._reqSigs: int = None
        self._type: str = None
        self._addresses: List[str] = []

    @property
    def asm(self) -> str:
        return self._asm

    @property
    def hex(self) -> str:
        return self._hex

    @property
    def reqSigs(self) -> int:
        return self._reqSigs

    @property
    def type(self) -> str:
        return self._type

    @property
    def addresses(self) -> List[str]:
        return self._addresses

    def set_asm(self, asm: str) -> None:
        self._asm = asm

    def set_hex(self, scripthex: str) -> None:
        self._hex = scripthex

    def set_reqSigs(self, reqSigs: int) -> None:
        self._reqSigs = reqSigs

    def set_type(self, stype: str) -> None:
        self._type = stype

    def set_addresses(self, addresses: List[str]) -> None:
        self._addresses = addresses

    def add_address(self, address: str) -> None:
        self._addresses.append(address)

    def fromJson(self, json: dict):
        if 'asm' in json:
            self.set_asm(json['asm'])
        if 'hex' in json:
            self.set_hex(json['hex'])
        if 'reqSigs' in json:
            self.set_reqSigs(json['reqSigs'])
        if 'type' in json:
            self.set_type(json['type'])
        if 'addresses' in json:
            self.set_addresses(json['addresses'])

    def toList(self) -> list:
        return [self.asm, self.hex, self.reqSigs, self.type, self.addresses]

    def toDict(self) -> dict:
        return {'asm': self.asm, 'hex': self.hex, 'reqSigs': self.reqSigs,
                'type': self.type, 'addresses': self.addresses}
