from typing import List


class MScriptPubKey():
    def __init__(self):
        self._asm: str = ''
        self._hex: str = ''
        self._reqSigs: int = -1
        self._type: str = ''
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

    def from_json(self, json: dict):
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

    def to_list(self) -> list:
        return [self.asm, self.hex, self.reqSigs, self.type, self.addresses]

    def to_dict(self) -> dict:
        return {'asm': self.asm, 'hex': self.hex, 'reqSigs': self.reqSigs,
                'type': self.type, 'addresses': self.addresses}
