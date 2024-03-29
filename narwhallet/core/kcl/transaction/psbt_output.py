from typing import Tuple
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction.psbt_types import record_types

from narwhallet.core.ksc.utils import Ut


class PsbtOutput():
    def __init__(self):
        self._PSBT_OUT_REDEEM_SCRIPT: bytes | None = None
        self._PSBT_OUT_WITNESS_SCRIPT: bytes | None = None
        self._PSBT_OUT_BIP32_DERIVATION: Tuple[bytes, bytes] | list | None = None
        self._PSBT_OUT_AMOUNT: bytes | None = None
        self._PSBT_OUT_SCRIPT: bytes | None = None
        self._PSBT_OUT_TAP_INTERNAL_KEY: bytes | None = None
        self._PSBT_OUT_TAP_TREE: bytes | None = None
        self._PSBT_OUT_TAP_LEAF_SCRIPT: bytes | None = None
        self._PSBT_OUT_TAP_BIP32_DERIVATION: Tuple[bytes, bytes] | list | None = None
        self._PSBT_OUT_PROPRIETARY: Tuple[bytes, bytes] | None = None
        self._UNKNOWN: Tuple[int, bytes, bytes] | None = None

    @property
    def PSBT_OUT_REDEEM_SCRIPT(self) -> bytes | None:
        return self._PSBT_OUT_REDEEM_SCRIPT

    @property
    def PSBT_OUT_WITNESS_SCRIPT(self) -> bytes | None:
        return self._PSBT_OUT_WITNESS_SCRIPT

    @property
    def PSBT_OUT_BIP32_DERIVATION(self) -> Tuple[bytes, bytes] | list | None:
        return self._PSBT_OUT_BIP32_DERIVATION

    @property
    def PSBT_OUT_AMOUNT(self) -> bytes | None:
        return self._PSBT_OUT_AMOUNT

    @property
    def PSBT_OUT_SCRIPT(self) -> bytes | None:
        return self._PSBT_OUT_SCRIPT

    @property
    def PSBT_OUT_TAP_INTERNAL_KEY(self) -> bytes | None:
        return self._PSBT_OUT_TAP_INTERNAL_KEY

    @property
    def PSBT_OUT_TAP_TREE(self) -> bytes | None:
        return self._PSBT_OUT_TAP_TREE

    @property
    def PSBT_OUT_TAP_LEAF_SCRIPT(self) -> bytes | None:
        return self._PSBT_OUT_TAP_LEAF_SCRIPT

    @property
    def PSBT_OUT_TAP_BIP32_DERIVATION(self) -> Tuple[bytes, bytes] | list | None:
        return self._PSBT_OUT_TAP_BIP32_DERIVATION

    @property
    def PSBT_OUT_PROPRIETARY(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_OUT_PROPRIETARY

    @property
    def UNKNOWN(self) -> Tuple[int, bytes, bytes] | None:
        return self._UNKNOWN

    def set_PSBT_OUT_REDEEM_SCRIPT(self, value: bytes) -> None:
        self._PSBT_OUT_REDEEM_SCRIPT = value
    
    def set_PSBT_OUT_WITNESS_SCRIPT(self, value: bytes) -> None:
        self._PSBT_OUT_WITNESS_SCRIPT = value
    
    def set_PSBT_OUT_BIP32_DERIVATION(self, key: bytes, value: bytes) -> None:
        if type(self._PSBT_OUT_BIP32_DERIVATION) == list:
            self._PSBT_OUT_BIP32_DERIVATION.append((key, value))
        elif self.PSBT_OUT_BIP32_DERIVATION is not None:
            self._PSBT_OUT_BIP32_DERIVATION = [self._PSBT_OUT_BIP32_DERIVATION, (key, value)]
        else:
            self._PSBT_OUT_BIP32_DERIVATION = (key, value)
    
    def set_PSBT_OUT_AMOUNT(self, value: bytes) -> None:
        self._PSBT_OUT_AMOUNT = value
    
    def set_PSBT_OUT_SCRIPT(self, value: bytes) -> None:
        self._PSBT_OUT_SCRIPT = value
    
    def set_PSBT_OUT_TAP_INTERNAL_KEY(self, value: bytes) -> None:
        self._PSBT_OUT_TAP_INTERNAL_KEY = value
    
    def set_PSBT_OUT_TAP_TREE(self, value: bytes) -> None:
        self._PSBT_OUT_TAP_TREE = value
    
    def set_PSBT_OUT_TAP_LEAF_SCRIPT(self, value: bytes) -> None:
        self._PSBT_OUT_TAP_LEAF_SCRIPT = value
    
    def set_PSBT_OUT_TAP_BIP32_DERIVATION(self, key: bytes, value: bytes) -> None:
        if type(self._PSBT_OUT_TAP_BIP32_DERIVATION) == list:
            self._PSBT_OUT_TAP_BIP32_DERIVATION.append((key, value))
        elif self.PSBT_OUT_TAP_BIP32_DERIVATION is not None:
            self._PSBT_OUT_TAP_BIP32_DERIVATION = [self._PSBT_OUT_TAP_BIP32_DERIVATION, (key, value)]
        else:
            self._PSBT_OUT_TAP_BIP32_DERIVATION = (key, value)
    
    def set_PSBT_OUT_PROPRIETARY(self, key: bytes, value: bytes) -> None:
        self._PSBT_OUT_PROPRIETARY = (key, value)

    def set_UNKNOWN(self, rec_type, key: bytes, value: bytes) -> None:
        self._UNKNOWN = (rec_type, key, value)

    def set_output(self, rec_type: str, key_data: bytes, value_data: bytes) -> None:
        if rec_type == 'PSBT_OUT_REDEEM_SCRIPT':
            self.set_PSBT_OUT_REDEEM_SCRIPT(value_data)
        elif rec_type == 'PSBT_OUT_WITNESS_SCRIPT':
            self.set_PSBT_OUT_WITNESS_SCRIPT(value_data)
        elif rec_type == 'PSBT_OUT_BIP32_DERIVATION':
            self.set_PSBT_OUT_BIP32_DERIVATION(key_data[1:], value_data)
        elif rec_type == 'PSBT_OUT_AMOUNT':
            self.set_PSBT_OUT_AMOUNT(value_data)
        elif rec_type == 'PSBT_OUT_SCRIPT':
            self.set_PSBT_OUT_SCRIPT(value_data)
        elif rec_type == 'PSBT_OUT_TAP_INTERNAL_KEY':
            self.set_PSBT_OUT_TAP_INTERNAL_KEY(value_data)
        elif rec_type == 'PSBT_OUT_TAP_TREE':
            self.set_PSBT_OUT_TAP_TREE(value_data)
        elif rec_type == 'PSBT_OUT_TAP_LEAF_SCRIPT':
            self.set_PSBT_OUT_TAP_LEAF_SCRIPT(value_data)
        elif rec_type == 'PSBT_OUT_TAP_BIP32_DERIVATION':
            self.set_PSBT_OUT_TAP_BIP32_DERIVATION(key_data[1:], value_data)
        elif rec_type == 'PSBT_OUT_PROPRIETARY':
            self.set_PSBT_OUT_PROPRIETARY(key_data[1:], value_data)
        else:
            self.set_UNKNOWN(rec_type, key_data[1:], value_data)

    def to_list(self, to_hex: bool = False) -> list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]]:
        _outputs: list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]] = []

        if self.PSBT_OUT_REDEEM_SCRIPT is not None:
            _outputs.append(['PSBT_OUT_REDEEM_SCRIPT', self.PSBT_OUT_REDEEM_SCRIPT])

        if self.PSBT_OUT_WITNESS_SCRIPT is not None:
            _outputs.append(['PSBT_OUT_WITNESS_SCRIPT', self.PSBT_OUT_WITNESS_SCRIPT])

        if self.PSBT_OUT_BIP32_DERIVATION is not None:
            if isinstance(self.PSBT_OUT_BIP32_DERIVATION, list):
                for i in self.PSBT_OUT_BIP32_DERIVATION:
                    _outputs.append(['PSBT_OUT_BIP32_DERIVATION', i])
            else:
                _outputs.append(['PSBT_OUT_BIP32_DERIVATION', self.PSBT_OUT_BIP32_DERIVATION])

        if self.PSBT_OUT_AMOUNT is not None:
            _outputs.append(['PSBT_OUT_AMOUNT', self.PSBT_OUT_AMOUNT])

        if self.PSBT_OUT_SCRIPT is not None:
            _outputs.append(['PSBT_OUT_SCRIPT', self.PSBT_OUT_SCRIPT])

        if self.PSBT_OUT_TAP_INTERNAL_KEY is not None:
            _outputs.append(['PSBT_OUT_TAP_INTERNAL_KEY', self.PSBT_OUT_TAP_INTERNAL_KEY])

        if self.PSBT_OUT_TAP_TREE is not None:
            _outputs.append(['PSBT_OUT_TAP_TREE', self.PSBT_OUT_TAP_TREE])

        if self.PSBT_OUT_TAP_LEAF_SCRIPT is not None:
            _outputs.append(['PSBT_OUT_TAP_LEAF_SCRIPT', self.PSBT_OUT_TAP_LEAF_SCRIPT])

        if self.PSBT_OUT_TAP_BIP32_DERIVATION is not None:
            if isinstance(self.PSBT_OUT_TAP_BIP32_DERIVATION, list):
                for i in self.PSBT_OUT_TAP_BIP32_DERIVATION:
                    _outputs.append(['PSBT_OUT_TAP_BIP32_DERIVATION', i])
            else:
                _outputs.append(['PSBT_OUT_TAP_BIP32_DERIVATION', self.PSBT_OUT_TAP_BIP32_DERIVATION])

        if self.PSBT_OUT_PROPRIETARY is not None:
            _outputs.append(['PSBT_OUT_PROPRIETARY', self.PSBT_OUT_PROPRIETARY])

        if self.UNKNOWN is not None:
            _outputs.append(['OUT UNKNOWN', self.UNKNOWN])

        if to_hex is True:
            _temp: list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]] = []
            for o in _outputs:
                if isinstance(o[1], bytes):
                    _temp.append([o[0], Ut.bytes_to_hex(o[1])])
                elif len(o[1]) == 2:
                    _temp.append([o[0], Ut.bytes_to_hex(o[1][0])])
                    _temp.append([o[0], Ut.bytes_to_hex(o[1][1])])
                elif len(o[1]) == 3:
                    _temp.append([o[0], o[1][0]])
                    _temp.append([o[0], Ut.bytes_to_hex(o[1][1])])
                    _temp.append([o[0], Ut.bytes_to_hex(o[1][2])])
            _outputs = _temp

        return _outputs

    def serialize(self) -> bytes:
        _pre = []
            
        if self.PSBT_OUT_REDEEM_SCRIPT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_REDEEM_SCRIPT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_REDEEM_SCRIPT)))
            _pre.append(self.PSBT_OUT_REDEEM_SCRIPT)

        if self.PSBT_OUT_WITNESS_SCRIPT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_WITNESS_SCRIPT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_WITNESS_SCRIPT)))
            _pre.append(self.PSBT_OUT_WITNESS_SCRIPT)

        if self.PSBT_OUT_BIP32_DERIVATION is not None:
            if isinstance(self.PSBT_OUT_BIP32_DERIVATION, list):
                for i in self.PSBT_OUT_BIP32_DERIVATION:
                    _bip = Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_BIP32_DERIVATION.value)
                    _bip = _bip + i[0]
                    _pre.append(Ut.to_cuint(len(_bip)))
                    _pre.append(_bip)
                    _pre.append(Ut.to_cuint(len(i[1])))
                    _pre.append(i[1])
            else:
                _bip = Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_BIP32_DERIVATION.value)
                _bip = _bip + self.PSBT_OUT_BIP32_DERIVATION[0]
                _pre.append(Ut.to_cuint(len(_bip)))
                _pre.append(_bip)
                _pre.append(Ut.to_cuint(len(self.PSBT_OUT_BIP32_DERIVATION[1])))
                _pre.append(self.PSBT_OUT_BIP32_DERIVATION[1])

        if self.PSBT_OUT_AMOUNT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_AMOUNT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_AMOUNT)))
            _pre.append(self.PSBT_OUT_AMOUNT)

        if self.PSBT_OUT_SCRIPT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_SCRIPT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_SCRIPT)))
            _pre.append(self.PSBT_OUT_SCRIPT)

        if self.PSBT_OUT_TAP_INTERNAL_KEY is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_TAP_INTERNAL_KEY.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_TAP_INTERNAL_KEY)))
            _pre.append(self.PSBT_OUT_TAP_INTERNAL_KEY)

        if self.PSBT_OUT_TAP_TREE is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_TAP_TREE.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_TAP_TREE)))
            _pre.append(self.PSBT_OUT_TAP_TREE)

        if self.PSBT_OUT_TAP_LEAF_SCRIPT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_TAP_LEAF_SCRIPT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_TAP_LEAF_SCRIPT)))
            _pre.append(self.PSBT_OUT_TAP_LEAF_SCRIPT)

        if self.PSBT_OUT_TAP_BIP32_DERIVATION is not None:
            if isinstance(self.PSBT_OUT_TAP_BIP32_DERIVATION, list):
                for i in self.PSBT_OUT_TAP_BIP32_DERIVATION:
                    _tbip = Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_TAP_BIP32_DERIVATION.value)
                    _tbip = _tbip + i[0]
                    _pre.append(Ut.to_cuint(len(_tbip)))
                    _pre.append(_tbip)
                    _pre.append(Ut.to_cuint(len(i[1])))
                    _pre.append(i[1])
            else:
                _tbip = Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_TAP_BIP32_DERIVATION.value)
                _tbip = _tbip + self.PSBT_OUT_TAP_BIP32_DERIVATION[0]
                _pre.append(Ut.to_cuint(len(_tbip)))
                _pre.append(_tbip)
                _pre.append(Ut.to_cuint(len(self.PSBT_OUT_TAP_BIP32_DERIVATION[1])))
                _pre.append(self.PSBT_OUT_TAP_BIP32_DERIVATION[1])

        if self.PSBT_OUT_PROPRIETARY is not None:
            _pro = Ut.to_cuint(record_types.OUTPUT.PSBT_OUT_PROPRIETARY.value)
            _pro = _pro + self.PSBT_OUT_PROPRIETARY[0]
            _pre.append(Ut.to_cuint(len(_pro)))
            _pre.append(_pro)
            _pre.append(Ut.to_cuint(len(self.PSBT_OUT_PROPRIETARY[1])))
            _pre.append(self.PSBT_OUT_PROPRIETARY[1])

        if self.UNKNOWN is not None:
            _pro = Ut.to_cuint(self.UNKNOWN[0])
            _pro = _pro + self.UNKNOWN[1]
            _pre.append(Ut.to_cuint(len(_pro)))
            _pre.append(_pro)
            _pre.append(Ut.to_cuint(len(self.UNKNOWN[2])))
            _pre.append(self.UNKNOWN[1])

        _pre.append(Ut.to_cuint(0))

        _spre = b''

        for p in _pre:
            _spre = _spre + p

        return _spre
