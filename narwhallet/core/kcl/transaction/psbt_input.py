from typing import Tuple
from narwhallet.core.kcl.transaction.builder.sighash import SIGHASH_TYPE
from narwhallet.core.kcl.transaction.psbt_types import record_types

from narwhallet.core.ksc.utils import Ut


class PsbtInput():
    def __init__(self):
        self._PSBT_IN_NON_WITNESS_UTXO: bytes | None = None
        self._PSBT_IN_WITNESS_UTXO: bytes | None = None
        self._PSBT_IN_PARTIAL_SIG: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_SIGHASH_TYPE: bytes | None = None
        self._PSBT_IN_REDEEM_SCRIPT: bytes | None = None
        self._PSBT_IN_WITNESS_SCRIPT: bytes | None = None
        self._PSBT_IN_BIP32_DERIVATION: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_FINAL_SCRIPTSIG: bytes | None = None
        self._PSBT_IN_FINAL_SCRIPTWITNESS: bytes | None = None
        self._PSBT_IN_POR_COMMITMENT: bytes | None = None
        self._PSBT_IN_RIPEMD160: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_SHA256: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_HASH160: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_HASH256: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_PREVIOUS_TXID: bytes | None = None
        self._PSBT_IN_OUTPUT_INDEX: bytes | None = None
        self._PSBT_IN_SEQUENCE: bytes | None = None
        self._PSBT_IN_REQUIRED_TIME_LOCKTIME: bytes | None = None
        self._PSBT_IN_REQUIRED_HEIGHT_LOCKTIME: bytes | None = None
        self._PSBT_IN_TAP_KEY_SIG: bytes | None = None
        self._PSBT_IN_TAP_SCRIPT_SIG: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_TAP_LEAF_SCRIPT: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_TAP_BIP32_DERIVATION: Tuple[bytes, bytes] | None = None
        self._PSBT_IN_TAP_INTERNAL_KEY: bytes | None = None
        self._PSBT_IN_TAP_MERKLE_ROOT: bytes | None = None
        self._PSBT_IN_PROPRIETARY: Tuple[bytes, bytes] | None = None
        self._UNKNOWN: Tuple[int, bytes, bytes] | None = None

    @property
    def PSBT_IN_NON_WITNESS_UTXO(self) -> bytes | None:
        return self._PSBT_IN_NON_WITNESS_UTXO
    
    @property
    def PSBT_IN_WITNESS_UTXO(self) -> bytes | None:
        return self._PSBT_IN_WITNESS_UTXO
    
    @property
    def PSBT_IN_PARTIAL_SIG(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_PARTIAL_SIG
    
    @property
    def PSBT_IN_SIGHASH_TYPE(self) -> bytes | None:
        return self._PSBT_IN_SIGHASH_TYPE
    
    @property
    def PSBT_IN_REDEEM_SCRIPT(self) -> bytes | None:
        return self._PSBT_IN_REDEEM_SCRIPT
    
    @property
    def PSBT_IN_WITNESS_SCRIPT(self) -> bytes | None:
        return self._PSBT_IN_WITNESS_SCRIPT
    
    @property
    def PSBT_IN_BIP32_DERIVATION(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_BIP32_DERIVATION
    
    @property
    def PSBT_IN_FINAL_SCRIPTSIG(self) -> bytes | None:
        return self._PSBT_IN_FINAL_SCRIPTSIG
    
    @property
    def PSBT_IN_FINAL_SCRIPTWITNESS(self) -> bytes | None:
        return self._PSBT_IN_FINAL_SCRIPTWITNESS
    
    @property
    def PSBT_IN_POR_COMMITMENT(self) -> bytes | None:
        return self._PSBT_IN_POR_COMMITMENT
    
    @property
    def PSBT_IN_RIPEMD160(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_RIPEMD160
    
    @property
    def PSBT_IN_SHA256(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_SHA256
    
    @property
    def PSBT_IN_HASH160(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_HASH160
    
    @property
    def PSBT_IN_HASH256(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_HASH256
    
    @property
    def PSBT_IN_PREVIOUS_TXID(self) -> bytes | None:
        return self._PSBT_IN_PREVIOUS_TXID
    
    @property
    def PSBT_IN_OUTPUT_INDEX(self) -> bytes | None:
        return self._PSBT_IN_OUTPUT_INDEX
    
    @property
    def PSBT_IN_SEQUENCE(self) -> bytes | None:
        return self._PSBT_IN_SEQUENCE
    
    @property
    def PSBT_IN_REQUIRED_TIME_LOCKTIME(self) -> bytes | None:
        return self._PSBT_IN_REQUIRED_TIME_LOCKTIME
    
    @property
    def PSBT_IN_REQUIRED_HEIGHT_LOCKTIME(self) -> bytes | None:
        return self._PSBT_IN_REQUIRED_HEIGHT_LOCKTIME
    
    @property
    def PSBT_IN_TAP_KEY_SIG(self) -> bytes | None:
        return self._PSBT_IN_TAP_KEY_SIG
    
    @property
    def PSBT_IN_TAP_SCRIPT_SIG(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_TAP_SCRIPT_SIG
    
    @property
    def PSBT_IN_TAP_LEAF_SCRIPT(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_TAP_LEAF_SCRIPT
    
    @property
    def PSBT_IN_TAP_BIP32_DERIVATION(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_TAP_BIP32_DERIVATION
    
    @property
    def PSBT_IN_TAP_INTERNAL_KEY(self) -> bytes | None:
        return self._PSBT_IN_TAP_INTERNAL_KEY
    
    @property
    def PSBT_IN_TAP_MERKLE_ROOT(self) -> bytes | None:
        return self._PSBT_IN_TAP_MERKLE_ROOT
    
    @property
    def PSBT_IN_PROPRIETARY(self) -> Tuple[bytes, bytes] | None:
        return self._PSBT_IN_PROPRIETARY

    @property
    def UNKNOWN(self) -> Tuple[int, bytes, bytes] | None:
        return self._UNKNOWN

    def set_PSBT_IN_NON_WITNESS_UTXO(self, value: bytes) -> None:
        self._PSBT_IN_NON_WITNESS_UTXO = value

    def set_PSBT_IN_WITNESS_UTXO(self, value: bytes) -> None:
        self._PSBT_IN_WITNESS_UTXO = value

    def set_PSBT_IN_PARTIAL_SIG(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_PARTIAL_SIG = (key, value)

    def set_PSBT_IN_SIGHASH_TYPE(self, value: bytes) -> None:
        self._PSBT_IN_SIGHASH_TYPE = value

    def set_PSBT_IN_REDEEM_SCRIPT(self, value: bytes) -> None:
        self._PSBT_IN_REDEEM_SCRIPT = value

    def set_PSBT_IN_WITNESS_SCRIPT(self, value: bytes) -> None:
        self._PSBT_IN_WITNESS_SCRIPT = value

    def set_PSBT_IN_BIP32_DERIVATION(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_BIP32_DERIVATION = (key, value)

    def set_PSBT_IN_FINAL_SCRIPTSIG(self, value: bytes) -> None:
        self._PSBT_IN_FINAL_SCRIPTSIG = value

    def set_PSBT_IN_FINAL_SCRIPTWITNESS(self, value: bytes) -> None:
        self._PSBT_IN_FINAL_SCRIPTWITNESS = value

    def set_PSBT_IN_POR_COMMITMENT(self, value: bytes) -> None:
        self._PSBT_IN_POR_COMMITMENT = value

    def set_PSBT_IN_RIPEMD160(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_RIPEMD160 = (key, value)

    def set_PSBT_IN_SHA256(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_SHA256 = (key, value)

    def set_PSBT_IN_HASH160(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_HASH160 = (key, value)

    def set_PSBT_IN_HASH256(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_HASH256 = (key, value)

    def set_PSBT_IN_PREVIOUS_TXID(self, value: bytes) -> None:
        self._PSBT_IN_PREVIOUS_TXID = value

    def set_PSBT_IN_OUTPUT_INDEX(self, value: bytes) -> None:
        self._PSBT_IN_OUTPUT_INDEX = value

    def set_PSBT_IN_SEQUENCE(self, value: bytes) -> None:
        self._PSBT_IN_SEQUENCE = value

    def set_PSBT_IN_REQUIRED_TIME_LOCKTIME(self, value: bytes) -> None:
        self._PSBT_IN_REQUIRED_TIME_LOCKTIME = value

    def set_PSBT_IN_REQUIRED_HEIGHT_LOCKTIME(self, value: bytes) -> None:
        self._PSBT_IN_REQUIRED_HEIGHT_LOCKTIME = value

    def set_PSBT_IN_TAP_KEY_SIG(self, value: bytes) -> None:
        self._PSBT_IN_TAP_KEY_SIG = value

    def set_PSBT_IN_TAP_SCRIPT_SIG(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_TAP_SCRIPT_SIG = (key, value)

    def set_PSBT_IN_TAP_LEAF_SCRIPT(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_TAP_LEAF_SCRIPT = (key, value)

    def set_PSBT_IN_TAP_BIP32_DERIVATION(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_TAP_BIP32_DERIVATION = (key, value)

    def set_PSBT_IN_TAP_INTERNAL_KEY(self, value: bytes) -> None:
        self._PSBT_IN_TAP_INTERNAL_KEY = value

    def set_PSBT_IN_TAP_MERKLE_ROOT(self, value: bytes) -> None:
        self._PSBT_IN_TAP_MERKLE_ROOT = value

    def set_PSBT_IN_PROPRIETARY(self, key: bytes, value: bytes) -> None:
        self._PSBT_IN_PROPRIETARY = (key, value)

    def set_UNKNOWN(self, rec_type, key: bytes, value: bytes) -> None:
        self._UNKNOWN = (rec_type, key, value)

    def set_input(self, rec_type: str, key_data: bytes, value_data: bytes) -> None:
        # print('inp rec_type', rec_type)
        if rec_type == 'PSBT_IN_NON_WITNESS_UTXO':
            self.set_PSBT_IN_NON_WITNESS_UTXO(value_data)
        elif rec_type == 'PSBT_IN_WITNESS_UTXO':
            self.set_PSBT_IN_WITNESS_UTXO(value_data)
        elif rec_type == 'PSBT_IN_PARTIAL_SIG':
            self.set_PSBT_IN_PARTIAL_SIG(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_SIGHASH_TYPE':
            self.set_PSBT_IN_SIGHASH_TYPE(value_data)
        elif rec_type == 'PSBT_IN_REDEEM_SCRIPT':
            self.set_PSBT_IN_REDEEM_SCRIPT(value_data)
        elif rec_type == 'PSBT_IN_WITNESS_SCRIPT':
            self.set_PSBT_IN_WITNESS_SCRIPT(value_data)
        elif rec_type == 'PSBT_IN_BIP32_DERIVATION':
            self.set_PSBT_IN_BIP32_DERIVATION(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_FINAL_SCRIPTSIG':
            self.set_PSBT_IN_FINAL_SCRIPTSIG(value_data)
        elif rec_type == 'PSBT_IN_FINAL_SCRIPTWITNESS':
            self.set_PSBT_IN_FINAL_SCRIPTWITNESS(value_data)
        elif rec_type == 'PSBT_IN_POR_COMMITMENT':
            self.set_PSBT_IN_POR_COMMITMENT(value_data)
        elif rec_type == 'PSBT_IN_RIPEMD160':
            self.set_PSBT_IN_RIPEMD160(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_SHA256':
            self.set_PSBT_IN_SHA256(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_HASH160':
            self.set_PSBT_IN_HASH160(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_HASH256':
            self.set_PSBT_IN_HASH256(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_PREVIOUS_TXID':
            self.set_PSBT_IN_PREVIOUS_TXID(value_data)
        elif rec_type == 'PSBT_IN_OUTPUT_INDEX':
            self.set_PSBT_IN_OUTPUT_INDEX(value_data)
        elif rec_type == 'PSBT_IN_SEQUENCE':
            self.set_PSBT_IN_SEQUENCE(value_data)
        elif rec_type == 'PSBT_IN_REQUIRED_TIME_LOCKTIME':
            self.set_PSBT_IN_REQUIRED_TIME_LOCKTIME(value_data)
        elif rec_type == 'PSBT_IN_REQUIRED_HEIGHT_LOCKTIME':
            self.set_PSBT_IN_REQUIRED_HEIGHT_LOCKTIME(value_data)
        elif rec_type == 'PSBT_IN_TAP_KEY_SIG':
            self.set_PSBT_IN_TAP_KEY_SIG(value_data)
        elif rec_type == 'PSBT_IN_TAP_SCRIPT_SIG':
            self.set_PSBT_IN_TAP_SCRIPT_SIG(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_TAP_LEAF_SCRIPT':
            self.set_PSBT_IN_TAP_LEAF_SCRIPT(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_TAP_BIP32_DERIVATION':
            self.set_PSBT_IN_TAP_BIP32_DERIVATION(key_data[1:], value_data)
        elif rec_type == 'PSBT_IN_TAP_INTERNAL_KEY':
            self.set_PSBT_IN_TAP_INTERNAL_KEY(value_data)
        elif rec_type == 'PSBT_IN_TAP_MERKLE_ROOT':
            self.set_PSBT_IN_TAP_MERKLE_ROOT(value_data)
        elif rec_type == 'PSBT_IN_PROPRIETARY':
            self.set_PSBT_IN_PROPRIETARY(key_data[1:], value_data)
        else:
            self.set_UNKNOWN(rec_type, key_data, value_data)

    def to_list(self, to_hex: bool = False) -> list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]]:
        _inputs: list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]] = []

        if self.PSBT_IN_NON_WITNESS_UTXO is not None:
            _inputs.append(['PSBT_IN_NON_WITNESS_UTXO', self.PSBT_IN_NON_WITNESS_UTXO])

        if self.PSBT_IN_WITNESS_UTXO is not None:
            _inputs.append(['PSBT_IN_WITNESS_UTXO', self.PSBT_IN_WITNESS_UTXO])

        if self.PSBT_IN_PARTIAL_SIG is not None:
            _inputs.append(['PSBT_IN_PARTIAL_SIG', self.PSBT_IN_PARTIAL_SIG])

        if self.PSBT_IN_SIGHASH_TYPE is not None:
            _inputs.append(['PSBT_IN_SIGHASH_TYPE', self.PSBT_IN_SIGHASH_TYPE])

        if self.PSBT_IN_REDEEM_SCRIPT is not None:
            _inputs.append(['PSBT_IN_REDEEM_SCRIPT', self.PSBT_IN_REDEEM_SCRIPT])

        if self.PSBT_IN_WITNESS_SCRIPT is not None:
            _inputs.append(['PSBT_IN_WITNESS_SCRIPT', self.PSBT_IN_WITNESS_SCRIPT])

        if self.PSBT_IN_BIP32_DERIVATION is not None:
            _inputs.append(['PSBT_IN_BIP32_DERIVATION', self.PSBT_IN_BIP32_DERIVATION])

        if self.PSBT_IN_FINAL_SCRIPTSIG is not None:
            _inputs.append(['PSBT_IN_FINAL_SCRIPTSIG', self.PSBT_IN_FINAL_SCRIPTSIG])

        if self.PSBT_IN_FINAL_SCRIPTWITNESS is not None:
            _inputs.append(['PSBT_IN_FINAL_SCRIPTWITNESS', self.PSBT_IN_FINAL_SCRIPTWITNESS])

        if self.PSBT_IN_POR_COMMITMENT is not None:
            _inputs.append(['PSBT_IN_POR_COMMITMENT', self.PSBT_IN_POR_COMMITMENT])

        if self.PSBT_IN_RIPEMD160 is not None:
            _inputs.append(['PSBT_IN_RIPEMD160', self.PSBT_IN_RIPEMD160])

        if self.PSBT_IN_SHA256 is not None:
            _inputs.append(['PSBT_IN_SHA256', self.PSBT_IN_SHA256])

        if self.PSBT_IN_HASH160 is not None:
            _inputs.append(['PSBT_IN_HASH160', self.PSBT_IN_HASH160])

        if self.PSBT_IN_HASH256 is not None:
            _inputs.append(['PSBT_IN_HASH256', self.PSBT_IN_HASH256])

        if self.PSBT_IN_PREVIOUS_TXID is not None:
            _inputs.append(['PSBT_IN_PREVIOUS_TXID', self.PSBT_IN_PREVIOUS_TXID])

        if self.PSBT_IN_OUTPUT_INDEX is not None:
            _inputs.append(['PSBT_IN_OUTPUT_INDEX', self.PSBT_IN_OUTPUT_INDEX])

        if self.PSBT_IN_SEQUENCE is not None:
            _inputs.append(['PSBT_IN_SEQUENCE', self.PSBT_IN_SEQUENCE])

        if self.PSBT_IN_REQUIRED_TIME_LOCKTIME is not None:
            _inputs.append(['PSBT_IN_REQUIRED_TIME_LOCKTIME', self.PSBT_IN_REQUIRED_TIME_LOCKTIME])

        if self.PSBT_IN_REQUIRED_HEIGHT_LOCKTIME is not None:
            _inputs.append(['PSBT_IN_REQUIRED_HEIGHT_LOCKTIME', self.PSBT_IN_REQUIRED_HEIGHT_LOCKTIME])

        if self.PSBT_IN_TAP_KEY_SIG is not None:
            _inputs.append(['PSBT_IN_TAP_KEY_SIG', self.PSBT_IN_TAP_KEY_SIG])

        if self.PSBT_IN_TAP_SCRIPT_SIG is not None:
            _inputs.append(['PSBT_IN_TAP_SCRIPT_SIG', self.PSBT_IN_TAP_SCRIPT_SIG])

        if self.PSBT_IN_TAP_LEAF_SCRIPT is not None:
            _inputs.append(['PSBT_IN_TAP_LEAF_SCRIPT', self.PSBT_IN_TAP_LEAF_SCRIPT])

        if self.PSBT_IN_TAP_BIP32_DERIVATION is not None:
            _inputs.append(['PSBT_IN_TAP_BIP32_DERIVATION', self.PSBT_IN_TAP_BIP32_DERIVATION])

        if self.PSBT_IN_TAP_INTERNAL_KEY is not None:
            _inputs.append(['PSBT_IN_TAP_INTERNAL_KEY', self.PSBT_IN_TAP_INTERNAL_KEY])

        if self.PSBT_IN_TAP_MERKLE_ROOT is not None:
            _inputs.append(['PSBT_IN_TAP_MERKLE_ROOT', self.PSBT_IN_TAP_MERKLE_ROOT])

        if self.PSBT_IN_PROPRIETARY is not None:
            _inputs.append(['PSBT_IN_PROPRIETARY', self.PSBT_IN_PROPRIETARY])

        if self.UNKNOWN is not None:
            _inputs.append(['UNKNOWN', self.UNKNOWN])

        if to_hex is True:
            _temp: list[list[str | bytes | Tuple[bytes, bytes] | Tuple[int, bytes, bytes]]] = []
            for i in _inputs:
                if isinstance(i[1], bytes):
                    _temp.append([i[0], Ut.bytes_to_hex(i[1])])
                elif len(i[1]) == 2:
                    _temp.append([i[0], Ut.bytes_to_hex(i[1][0])])
                    _temp.append([i[0], Ut.bytes_to_hex(i[1][1])])
                elif len(i[1]) == 3:
                    _temp.append([i[0], i[1][0]])
                    _temp.append([i[0], Ut.bytes_to_hex(i[1][1])])
                    _temp.append([i[0], Ut.bytes_to_hex(i[1][2])])
            _inputs = _temp

        return _inputs

    def serialize(self) -> bytes:
        _pre = []

        if self.PSBT_IN_NON_WITNESS_UTXO is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_NON_WITNESS_UTXO.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_NON_WITNESS_UTXO)))
            _pre.append(self.PSBT_IN_NON_WITNESS_UTXO)

        if self.PSBT_IN_WITNESS_UTXO is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_WITNESS_UTXO.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_WITNESS_UTXO)))
            _pre.append(self.PSBT_IN_WITNESS_UTXO)

        if self.PSBT_IN_PARTIAL_SIG is not None:
            _sig = Ut.to_cuint(record_types.INPUT.PSBT_IN_PARTIAL_SIG.value)
            # _PSBT_IN_PARTIAL_SIG '02'
            # TODO: Find better way to handle the sort

            # if len(_sig_data.stack) == 2:
            _sig = _sig + self.PSBT_IN_PARTIAL_SIG[0]
            _pre.append(Ut.to_cuint(len(_sig)))
            _pre.append(_sig)
            _sig_bytes = self.PSBT_IN_PARTIAL_SIG[1]
            _pre.append(Ut.to_cuint(len(_sig_bytes)))
            _pre.append(_sig_bytes)
            # else:
            #     for _stack_item in _sig_data.stack:
            #         _pre.append(Ut.to_cuint(len(_stack_item)))
            #         _pre.append(_stack_item)

        if self.PSBT_IN_SIGHASH_TYPE is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_SIGHASH_TYPE.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_SIGHASH_TYPE)))
            _pre.append(self.PSBT_IN_SIGHASH_TYPE)

        if self.PSBT_IN_REDEEM_SCRIPT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_REDEEM_SCRIPT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_REDEEM_SCRIPT)))
            _pre.append(self.PSBT_IN_REDEEM_SCRIPT)

        if self.PSBT_IN_WITNESS_SCRIPT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_WITNESS_SCRIPT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_WITNESS_SCRIPT)))
            _pre.append(self.PSBT_IN_WITNESS_SCRIPT)

        if self.PSBT_IN_BIP32_DERIVATION is not None:
            _bipd = Ut.to_cuint(record_types.INPUT.PSBT_IN_BIP32_DERIVATION.value)
            _bipd = _bipd + self.PSBT_IN_BIP32_DERIVATION[0]
            _pre.append(Ut.to_cuint(len(_bipd)))
            _pre.append(_bipd)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_BIP32_DERIVATION[1])))
            _pre.append(self.PSBT_IN_BIP32_DERIVATION[1])

        if self.PSBT_IN_FINAL_SCRIPTSIG is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_FINAL_SCRIPTSIG.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_FINAL_SCRIPTSIG)))
            _pre.append(self.PSBT_IN_FINAL_SCRIPTSIG)

        if self.PSBT_IN_FINAL_SCRIPTWITNESS is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_FINAL_SCRIPTWITNESS.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_FINAL_SCRIPTWITNESS)))
            _pre.append(self.PSBT_IN_FINAL_SCRIPTWITNESS)

        if self.PSBT_IN_POR_COMMITMENT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_POR_COMMITMENT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_POR_COMMITMENT)))
            _pre.append(self.PSBT_IN_POR_COMMITMENT)

        if self.PSBT_IN_RIPEMD160 is not None:
            _ripe = Ut.to_cuint(record_types.INPUT.PSBT_IN_RIPEMD160.value)
            _ripe = _ripe + self.PSBT_IN_RIPEMD160[0]
            _pre.append(Ut.to_cuint(len(_ripe)))
            _pre.append(_ripe)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_RIPEMD160[1])))
            _pre.append(self.PSBT_IN_RIPEMD160[1])

        if self.PSBT_IN_SHA256 is not None:
            _sha = Ut.to_cuint(record_types.INPUT.PSBT_IN_SHA256.value)
            _sha = _sha + self.PSBT_IN_SHA256[0]
            _pre.append(Ut.to_cuint(len(_sha)))
            _pre.append(_sha)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_SHA256[1])))
            _pre.append(self.PSBT_IN_SHA256[1])

        if self.PSBT_IN_HASH160 is not None:
            _hash = Ut.to_cuint(record_types.INPUT.PSBT_IN_HASH160.value)
            _hash = _hash + self.PSBT_IN_HASH160[0]
            _pre.append(Ut.to_cuint(len(_hash)))
            _pre.append(_hash)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_HASH160[1])))
            _pre.append(self.PSBT_IN_HASH160[1])

        if self.PSBT_IN_HASH256 is not None:
            _hash = Ut.to_cuint(record_types.INPUT.PSBT_IN_HASH256.value)
            _hash = _hash + self.PSBT_IN_HASH256[0]
            _pre.append(Ut.to_cuint(len(_hash)))
            _pre.append(_hash)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_HASH256[1])))
            _pre.append(self.PSBT_IN_HASH256[1])

        if self.PSBT_IN_PREVIOUS_TXID is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_PREVIOUS_TXID.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_PREVIOUS_TXID)))
            _pre.append(self.PSBT_IN_PREVIOUS_TXID)

        if self.PSBT_IN_OUTPUT_INDEX is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_OUTPUT_INDEX.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_OUTPUT_INDEX)))
            _pre.append(self.PSBT_IN_OUTPUT_INDEX)

        if self.PSBT_IN_SEQUENCE is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_SEQUENCE.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_SEQUENCE)))
            _pre.append(self.PSBT_IN_SEQUENCE)

        if self.PSBT_IN_REQUIRED_TIME_LOCKTIME is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_REQUIRED_TIME_LOCKTIME.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_REQUIRED_TIME_LOCKTIME)))
            _pre.append(self.PSBT_IN_REQUIRED_TIME_LOCKTIME)

        if self.PSBT_IN_REQUIRED_HEIGHT_LOCKTIME is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_REQUIRED_HEIGHT_LOCKTIME.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_REQUIRED_HEIGHT_LOCKTIME)))
            _pre.append(self.PSBT_IN_REQUIRED_HEIGHT_LOCKTIME)

        if self.PSBT_IN_TAP_KEY_SIG is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_TAP_KEY_SIG.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_TAP_KEY_SIG)))
            _pre.append(self.PSBT_IN_TAP_KEY_SIG)

        if self.PSBT_IN_TAP_SCRIPT_SIG is not None:
            _tsig = Ut.to_cuint(record_types.INPUT.PSBT_IN_TAP_SCRIPT_SIG.value)
            _tsig = _tsig + self.PSBT_IN_TAP_SCRIPT_SIG[0]
            _pre.append(Ut.to_cuint(len(_tsig)))
            _pre.append(_tsig)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_TAP_SCRIPT_SIG[1])))
            _pre.append(self.PSBT_IN_TAP_SCRIPT_SIG[1])

        if self.PSBT_IN_TAP_LEAF_SCRIPT is not None:
            _leaf = Ut.to_cuint(record_types.INPUT.PSBT_IN_TAP_LEAF_SCRIPT.value)
            _leaf = _leaf + self.PSBT_IN_TAP_LEAF_SCRIPT[0]
            _pre.append(Ut.to_cuint(len(_leaf)))
            _pre.append(_leaf)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_TAP_LEAF_SCRIPT[1])))
            _pre.append(self.PSBT_IN_TAP_LEAF_SCRIPT[1])

        if self.PSBT_IN_TAP_BIP32_DERIVATION is not None:
            _tbip = Ut.to_cuint(record_types.INPUT.PSBT_IN_TAP_BIP32_DERIVATION.value)
            _tbip = _tbip + self.PSBT_IN_TAP_BIP32_DERIVATION[0]
            _pre.append(Ut.to_cuint(len(_tbip)))
            _pre.append(_tbip)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_TAP_BIP32_DERIVATION[1])))
            _pre.append(self.PSBT_IN_TAP_BIP32_DERIVATION[1])

        if self.PSBT_IN_TAP_INTERNAL_KEY is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_TAP_INTERNAL_KEY.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_TAP_INTERNAL_KEY)))
            _pre.append(self.PSBT_IN_TAP_INTERNAL_KEY)

        if self.PSBT_IN_TAP_MERKLE_ROOT is not None:
            _pre.append(Ut.to_cuint(1))
            _pre.append(Ut.to_cuint(record_types.INPUT.PSBT_IN_TAP_MERKLE_ROOT.value))
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_TAP_MERKLE_ROOT)))
            _pre.append(self.PSBT_IN_TAP_MERKLE_ROOT)

        if self.PSBT_IN_PROPRIETARY is not None:
            _pro = Ut.to_cuint(record_types.INPUT.PSBT_IN_PROPRIETARY.value)
            _pro = _pro + self.PSBT_IN_PROPRIETARY[0]
            _pre.append(Ut.to_cuint(len(_pro)))
            _pre.append(_pro)
            _pre.append(Ut.to_cuint(len(self.PSBT_IN_PROPRIETARY[1])))
            _pre.append(self.PSBT_IN_PROPRIETARY[1])

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
